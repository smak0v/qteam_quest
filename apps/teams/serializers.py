from django.utils import timezone
from rest_framework import serializers

from apps.games.models import Game
from apps.games.serializers import GameSerializer
from apps.teams.models import Team, UserInTeam, TemporaryReserve
from users.models import User
from users.serializers import UserSerializer


class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    """Class that represents a team create, update serializer"""

    class Meta:
        model = Team
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    """Class that represents a team serializer"""

    game = GameSerializer()

    class Meta:
        model = Team
        fields = '__all__'


class UserInTeamCreateSerializer(serializers.ModelSerializer):
    """Class that represents user in a team create, update serializer"""

    class Meta:
        model = UserInTeam
        fields = [
            'user',
            'title',
        ]

    def validate(self, data):
        # TODO validate
        # user_from_request = data.get('user')
        # game_from_request = data.get('game')
        # try:
        #     user_in_game = UserInTeam.objects.get(user=user_from_request, game=game_from_request)
        #
        # except UserInTeam.DoesNotExist:
        #     data['team'] = Team.objects.get(game=game_from_request)
        #     game = Game.objects.get(pk=game_from_request.pk)
        #     if game.players_count == game.max_players_count:
        #         raise serializers.ValidationError({
        #             'error': 'No empty places for this game!',
        #         })
        #     game.players_count += 1
        #     game.save()
        return data


class UserInTeamSerializer(serializers.ModelSerializer):
    """Class that represents user in a team serializer"""

    game = GameSerializer()
    team = TeamSerializer()
    user = UserSerializer()

    class Meta:
        model = UserInTeam
        fields = '__all__'


class TemporaryReserveSerializer(serializers.ModelSerializer):
    """Class that implements temporary reserve serializer"""

    class Meta:
        model = TemporaryReserve
        fields = '__all__'
