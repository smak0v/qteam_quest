from rest_framework import serializers

from apps.games.models import Game


class PaymentSuccessSerializer(serializers.Serializer):
    """Class that implements payment success serializer"""

    game_id = serializers.IntegerField()

    def validate(self, data):
        try:
            game = Game.objects.get(pk=data['game_id'])
        except Game.DoesNotExist:
            raise serializers.ValidationError({
                'game_id': f'Game with id {data["game_id"]} does not exist!',
            })
        return data
