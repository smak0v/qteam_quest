from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Game


class GameConsumer(AsyncWebsocketConsumer):
    """Class that implements game websocket consumer"""

    async def connect(self):
        self.game_pk = self.scope['url_route']['kwargs']['pk']
        try:
            game = Game.objects.get(pk=self.game_pk)
        except Game.DoesNotExist:
            await self.close()
        self.game_group_name = str(self.game_pk)
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': message,
            }
        )

    async def game_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))
