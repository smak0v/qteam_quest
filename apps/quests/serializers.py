from rest_framework import serializers

from apps.quests.models import Quest, QuestComment, QuestSubscription, MetroStation, QuestImage
from qteam_quest.settings import ROOT_URL
from users.serializers import UserSerializer


class MetroStationSerializer(serializers.ModelSerializer):
    """Class that represents metro station serializer"""

    class Meta:
        model = MetroStation
        fields = [
            'name',
            'color',
        ]


class QuestImageSerializer(serializers.ModelSerializer):
    """Class that implements quest image serializer"""

    image = serializers.SerializerMethodField()

    @staticmethod
    def get_image(quest_image):
        return ROOT_URL + quest_image.image.url

    class Meta:
        model = QuestImage
        fields = [
            'image',
            'uploading_timespan',
        ]


class QuestSerializer(serializers.ModelSerializer):
    """Class that represents quest serializer"""

    metro_stations = MetroStationSerializer(
        many=True,
        read_only=True
    )
    cover_image = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    @staticmethod
    def get_cover_image(quest):
        if not quest.cover_image:
            return None
        return ROOT_URL + quest.cover_image.url

    @staticmethod
    def get_photo(quest):
        if not quest.photo:
            return None
        return ROOT_URL + quest.photo.url

    class Meta:
        model = Quest
        fields = '__all__'


class QuestUpdateSerializer(serializers.ModelSerializer):
    """Class that represents quest update serializer"""

    name = serializers.CharField(
        max_length=255,
        required=False,
    )
    phone = serializers.CharField(
        max_length=15,
        required=False,
    )
    location = serializers.CharField(
        max_length=255,
        required=False,
    )
    x_coordinate = serializers.DecimalField(
        decimal_places=5,
        max_digits=7,
        required=False,
    )
    y_coordinate = serializers.DecimalField(
        decimal_places=5,
        max_digits=7,
        required=False,
    )

    class Meta:
        model = Quest
        exclude = [
            'rating',
        ]


class QuestCommentCreateSerializer(serializers.ModelSerializer):
    """Class that represents quest comment create serializer"""

    class Meta:
        model = QuestComment
        fields = '__all__'

    def create(self, validated_data):
        quest_comment = QuestComment.objects.create(**validated_data)
        quest = validated_data.get('quest')
        quest_obj = Quest.objects.get(pk=quest.pk)
        quest_comments = QuestComment.objects.filter(quest=quest)
        scores_sum = 0
        for quest_comment in quest_comments:
            scores_sum += int(quest_comment.scores)
        quest_obj.rating = float(scores_sum / len(quest_comments))
        quest_obj.save()
        return quest_comment


class QuestCommentSerializer(serializers.ModelSerializer):
    """Class that represents quest comment serializer"""

    user = UserSerializer()
    quest = QuestSerializer()

    class Meta:
        model = QuestComment
        fields = '__all__'


class QuestSubscriptionCreateSerializer(serializers.ModelSerializer):
    """Class that represents quest subscription create serializer"""

    class Meta:
        model = QuestSubscription
        fields = '__all__'


class QuestSubscriptionSerializer(serializers.ModelSerializer):
    """Class that represents quest subscription serializer"""

    user = UserSerializer()
    quest = QuestSerializer()

    class Meta:
        model = QuestSubscription
        fields = '__all__'
