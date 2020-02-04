from rest_framework import serializers

from apps.timeline.models import TimelineBlock


class TimelineBlockSerializer(serializers.ModelSerializer):
    """Class that implements timeline block element serializer"""

    class Meta:
        model = TimelineBlock
        fields = '__all__'
