from rest_framework import serializers

from apps.venues.models import Venue, VenueComment, VenueSubscription, MetroStation
from users.serializers import UserSerializer
from qteam_quest.settings import ROOT_URL


class MetroStationSerializer(serializers.ModelSerializer):
    """Class that represents metro station serializer"""

    class Meta:
        model = MetroStation
        fields = ['name', 'color']


class VenueSerializer(serializers.ModelSerializer):
    """Class that represents venue serializer"""
    metro_stations = MetroStationSerializer(many=True, read_only=True)
    cover_image = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    @staticmethod
    def get_cover_image(venue):
        if not venue.cover_image:
            return None
        return ROOT_URL + venue.cover_image.url

    @staticmethod
    def get_photo(venue):
        if not venue.photo:
            return None
        return ROOT_URL + venue.photo.url

    class Meta:
        model = Venue
        fields = '__all__'


class VenueCommentCreateUpdateSerializer(serializers.ModelSerializer):
    """Class that represents venue comment create, update serializer"""

    class Meta:
        model = VenueComment
        fields = '__all__'

    def create(self, validated_data):
        venue_comment = VenueComment.objects.create(**validated_data)
        venue = validated_data.get('venue')
        venue_obj = Venue.objects.get(pk=venue.pk)
        venue_comments = VenueComment.objects.filter(venue=venue)
        scores_sum = 0
        for venue_comment in venue_comments:
            scores_sum += int(venue_comment.scores)
        venue_obj.rating = float(scores_sum / len(venue_comments))
        venue_obj.save()
        return venue_comment


class VenueCommentSerializer(serializers.ModelSerializer):
    """Class that represents venue comment serializer"""

    user = UserSerializer()
    venue = VenueSerializer()

    class Meta:
        model = VenueComment
        fields = '__all__'


class VenueSubscriptionCreateSerializer(serializers.ModelSerializer):
    """Class that represents venue subscription create serializer"""

    class Meta:
        model = VenueSubscription
        fields = '__all__'

    def validate(self, data):
        try:
            venue_subscription = VenueSubscription.objects.get(user=data['user'], venue=data['venue'])
            raise serializers.ValidationError('Venue subscription already exists!')
        except VenueSubscription.DoesNotExist:
            return data


class VenueSubscriptionSerializer(serializers.ModelSerializer):
    """Class that represents venue subscription serializer"""

    user = UserSerializer()
    venue = VenueSerializer()

    class Meta:
        model = VenueSubscription
        fields = '__all__'
