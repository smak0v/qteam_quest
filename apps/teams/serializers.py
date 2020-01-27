from rest_framework import serializers

from apps.games.serializers import GameSerializer
from apps.teams.models import Team, UserInTeam, TemporaryReserve
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
