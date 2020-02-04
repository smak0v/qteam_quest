from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.timeline.models import TimelineBlock
from apps.timeline.serializers import TimelineBlockSerializer
from users.models import User


class TimelineAPIView(APIView):
    """Class that implements timeline retrieve view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return Response({
                'error': 'User does not exist!',
            }, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user != user:
            return Response({
                'error': 'User from request must be the same user from url!',
            }, status=status.HTTP_400_BAD_REQUEST)
        timeline_blocks = TimelineBlock.objects.filter(user=user).order_by('-timespan')[:20]
        return Response({
            'timeline': TimelineBlockSerializer(timeline_blocks, many=True).data,
        }, status=status.HTTP_200_OK)
