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


class UserInTeamCreateSerializer(serializers.ModelSerializer):
    """Class that represents user in a team create, update serializer"""

    class Meta:
        model = UserInTeam
        fields = [
            'user',
            'game',
        ]

    def validate(self, data):
        user_from_request = data.get('user')
        game_from_request = data.get('game')
        try:
            user_in_game = UserInTeam.objects.get(user=user_from_request, game=game_from_request)
            if user_in_game is not None:
                raise serializers.ValidationError({
                    'user': 'User already registered for this game!',
                })
        except UserInTeam.DoesNotExist:
            data['team'] = Team.objects.get(game=game_from_request)
            game = Game.objects.get(pk=game_from_request.pk)
            if game.players_count == game.max_players_count:
                raise serializers.ValidationError({
                    'error': 'No empty places for this game!',
                })
            game.players_count += 1
            game.save()
            return data


class UserInTeamSerializer(serializers.ModelSerializer):
    """Class that represents user in a team serializer"""

    game = GameSerializer()
    team = TeamSerializer()
    user = UserSerializer()

    class Meta:
        model = UserInTeam
        fields = '__all__'


class ReservedPlaceInTeamCreateSerializer(serializers.Serializer):
    """Class that represents reserved place in a team for user by another user create, update serializer"""

    title = serializers.CharField(
        required=True,
    )
    game = serializers.IntegerField(
        required=True,
    )
    user = serializers.IntegerField(
        required=True,
    )
    count = serializers.IntegerField(
        required=True,
    )

    def validate(self, data):
        try:
            UserInTeam.objects.get(user=User.objects.get(pk=data.get('user')),
                                   game=Game.objects.get(pk=data.get('game')))
        except UserInTeam.DoesNotExist:
            raise serializers.ValidationError({
                'user': 'User must be the participant of the game!',
            })
        data['team'] = Team.objects.get(game=data.get('game'))
        game = Game.objects.get(pk=data.get('game'))
        if game.players_count == game.max_players_count:
            raise serializers.ValidationError({
                'error': 'No empty places for this game!',
            })
        if data.get('count') <= 0:
            raise serializers.ValidationError({
                'error': 'Count field can not be less than 1!',
            })
        if data.get('count') > game.max_players_count - game.players_count:
            raise serializers.ValidationError({
                'error': f'You can reserve no more than {game.max_players_count - game.players_count} places!',
            })
        return data


class ReservedPlaceInTeamSerializer(serializers.ModelSerializer):
    """Class that represents reserved place in a team for user by another user"""

    game = GameSerializer()
    team = TeamSerializer()
    user = UserSerializer()

    class Meta:
        model = ReservedPlaceInTeam
        fields = '__all__'
