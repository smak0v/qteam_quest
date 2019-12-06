from rest_framework import serializers

from apps.games.models import Game
from apps.games.serializers import GameSerializer
from apps.teams.models import Team, UserInTeam, ReservedPlaceInTeam
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


class UserInTeamCreateUpdateSerializer(serializers.ModelSerializer):
    """Class that represents user in a team create, update serializer"""

    class Meta:
        model = UserInTeam
        fields = '__all__'

    def validate(self, data):
        user_from_request = data.get('user')
        game_from_request = data.get('game')
        user_position = data.get('user_position')
        user_in_game = None
        if user_position == 'NOT_SET':
            raise serializers.ValidationError('You need to choose the position in game!')
        try:
            user_in_game = UserInTeam.objects.get(user=user_from_request, game=game_from_request)
            if user_in_game is not None:
                raise serializers.ValidationError('User already registered for this game!')
        except UserInTeam.DoesNotExist:
            return data


class UserInTeamSerializer(serializers.ModelSerializer):
    """Class that represents user in a team serializer"""

    game = GameSerializer()
    team = TeamSerializer()
    user = UserSerializer()

    class Meta:
        model = UserInTeam
        fields = '__all__'


class ReservedPlaceInTeamCreateUpdateSerializer(serializers.ModelSerializer):
    """Class that represents reserved place in a team for user by another user create, update serializer"""

    class Meta:
        model = ReservedPlaceInTeam
        fields = '__all__'

    def validate(self, data):
        try:
            player = UserInTeam.objects.get(user=User.objects.get(pk=data.get('user').pk),
                                            game=Game.objects.get(pk=data.get('game').pk))
        except UserInTeam.DoesNotExist:
            raise serializers.ValidationError('User must be the participant of the game!')
        if data.get('reserved_position') == 'NOT_SET':
            raise serializers.ValidationError('You need to choose the position in game!')
        return data


class ReservedPlaceInTeamSerializer(serializers.ModelSerializer):
    """Class that represents reserved place in a team for user by another user"""

    game = GameSerializer()
    team = TeamSerializer()
    user = UserSerializer()

    class Meta:
        model = ReservedPlaceInTeam
        fields = '__all__'
