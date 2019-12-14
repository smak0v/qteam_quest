from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from apps.quests.models import Game
from apps.quests.serializers import GameSerializer
from apps.venues.models import Venue, VenueSubscription, VenueComment
from apps.venues.serializers import VenueSerializer, VenueSubscriptionSerializer, VenueCommentSerializer, \
    VenueCommentCreateSerializer, VenueSubscriptionCreateSerializer
from users.models import User
from users.serializers import UserSerializer


class VenueListCreateView(ListCreateAPIView):
    """Class that implements venue create, list view API endpoint"""

    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Class that implements venue retrieve, update, destroy view API endpoint"""

    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    def retrieve(self, request, pk):
        user = self.request.user
        try:
            venue = Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            return Response({
                'error': 'Venue does not exists!',
            })
        response = {
            'venue': VenueSerializer(venue).data,
        }
        if user.is_authenticated:
            try:
                VenueSubscription.objects.get(user=user, venue=venue)
                response['subscription'] = 'subscribed'
            except VenueSubscription.DoesNotExist:
                response['subscription'] = 'not_subscribed'
        return Response(response)


class VenueSubscribersListView(ListCreateAPIView):
    """Class that implements venue subscribers create, list view API endpoint"""

    queryset = VenueSubscription.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @staticmethod
    def get(request, pk):
        venue_subscriptions = VenueSubscription.objects.filter(venue=pk)
        users = list()
        for venue_subscription in venue_subscriptions:
            users.append(User.objects.get(pk=venue_subscription.user.pk))
        data = UserSerializer(users, many=True).data
        return Response(data)


class VenueGamesListView(ListAPIView):
    """Class that implements venue`s quests list view API endpoint"""

    queryset = VenueSubscription.objects.all()

    @staticmethod
    def get(request, *args, **kwargs):
        games = Game.objects.filter(venue=kwargs.get('pk'))
        data = GameSerializer(games, many=True).data
        return Response({
            'games': data,
            'count': int(games.count()),
        })


class VenueSubscribeCreateView(CreateAPIView):
    """Class that implements venue subscription create view API endpoint"""

    queryset = VenueSubscription.objects.all()
    serializer_class = VenueSubscriptionCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class VenueSubscribeDestroyView(DestroyAPIView):
    """Class that implements venue subscription destroy view API endpoint"""

    queryset = VenueSubscription.objects.all()
    serializer_class = VenueSubscriptionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def destroy(request, *args, **kwargs):
        try:
            user = request.data['user']
        except KeyError:
            raise ValidationError({
                'user': 'Required field!',
            })
        try:
            venue = request.data['venue']
        except KeyError:
            raise ValidationError({
                'venue': 'Required field!',
            })
        venue_subscription = VenueSubscription.objects.get(user=user, venue=venue)
        if not venue_subscription:
            return Response({
                'message': 'Venue subscription does not exists!',
            }, status=status.HTTP_404_NOT_FOUND)
        venue_subscription.delete()
        return Response({
            'message': 'Venue subscription successfully deleted!',
        }, status=status.HTTP_200_OK)


class VenueCommentListCreateView(ListCreateAPIView):
    """Class that implements venue comment list, create view API endpoint"""

    queryset = VenueComment.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VenueCommentCreateSerializer
        return VenueCommentSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        venue_comments = VenueComment.objects.filter(venue=kwargs.get('pk'))
        data = VenueCommentSerializer(venue_comments, many=True).data
        return Response({
            'comments': data,
            'count': int(venue_comments.count()),
        }, status=status.HTTP_200_OK)
