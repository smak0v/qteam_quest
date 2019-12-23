from rest_framework import serializers

from apps.games.models import Game, GameComment, GamePlayerEvaluation
from apps.quests.models import Quest
from apps.quests.serializers import QuestSerializer
from apps.teams.models import Team, UserInTeam
from qteam_quest.settings import ROOT_URL
from users.serializers import UserSerializer


class GameCreateUpdateSerializer(serializers.ModelSerializer):
    """Class that represents game create, update serializer"""

    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
        game = Game.objects.create(**validated_data)
        Team.objects.create(
            game=game,
        )
        return game

    @staticmethod
    def validate_price(price):
        if price < 0:
            raise serializers.ValidationError('Prise can`t be less than 0!')
        return price


class GameSerializer(serializers.ModelSerializer):
    """Class that represents game serializer"""

    quest = QuestSerializer()
    cover_image = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    @staticmethod
    def get_cover_image(game):
        if not game.cover_image:
            return None
        return ROOT_URL + game.cover_image.url

    @staticmethod
    def get_photo(game):
        if not game.photo:
            return None
        return ROOT_URL + game.photo.url

    class Meta:
        model = Game
        fields = '__all__'


class GameCommentCreateSerializer(serializers.ModelSerializer):
    """Class that represents game comment create serializer"""

    class Meta:
        model = GameComment
        fields = '__all__'


class GameCommentSerializer(serializers.ModelSerializer):
    """Class that represents game comment serializer"""

    user = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = GameComment
        fields = '__all__'


class GamePlayerEvaluationCreateSerializer(serializers.ModelSerializer):
    """Class that represents game player evaluation create serializer"""

    class Meta:
        model = GamePlayerEvaluation
        fields = '__all__'

    def validate(self, data):
        try:
            appraiser = UserInTeam.objects.get(user=data['appraiser'], game=data['game'])
        except UserInTeam.DoesNotExist:
            raise serializers.ValidationError('Appraiser must participate in the game!')
        try:
            ranked_user = UserInTeam.objects.get(user=data['ranked_user'], game=data['game'])
        except UserInTeam.DoesNotExist:
            raise serializers.ValidationError('Ranked user must participate in the game!')
        if data['appraiser'] == data['ranked_user']:
            raise serializers.ValidationError('Appraiser should not be ranked user!')
        return data

    def create(self, validated_data):
        player_valuation = GamePlayerEvaluation.objects.create(**validated_data)
        ranked_user = UserInTeam.objects.get(user=validated_data['ranked_user'], game=validated_data['game'])
        ranked_user.reliability = self.update_ranked_user_reliability(ranked_user)
        ranked_user.save()
        return player_valuation

    @staticmethod
    def update_ranked_user_reliability(ranked_user):
        return 100
