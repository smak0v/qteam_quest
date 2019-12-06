from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from apps.games.models import Game
from apps.games.serializers import GameSerializer
from apps.venues.models import Venue, VenueSubscription, VenueComment
from apps.venues.serializers import VenueSerializer, VenueSubscriptionSerializer, VenueCommentSerializer, \
    VenueCommentCreateUpdateSerializer, VenueSubscriptionCreateSerializer
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
                user_venue_subscription = VenueSubscription.objects.get(user=user, venue=venue)
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
    """Class that implements venue`s games list view API endpoint"""

    queryset = VenueSubscription.objects.all()

    @staticmethod
    def get(request, pk):
        games = Game.objects.filter(venue=pk)
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
    def destroy(request, pk):
        try:
            venue_subscription = VenueSubscription.objects.get(user=request.POST['user'],
                                                               venue=request.POST['venue'])
            venue_subscription.delete()
            return Response({
                'message': 'Venue subscription successfully deleted!',
            })
        except VenueSubscription.DoesNotExist:
            return Response({
                'message': 'Venue subscription does not exists!',
            })


class VenueCommentListCreateView(ListCreateAPIView):
    """Class that implements venue comment list, create view API endpoint"""

    queryset = VenueComment.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'UPDATE':
            return VenueCommentCreateUpdateSerializer
        return VenueCommentSerializer

    @staticmethod
    def get(request, pk):
        venue_comments = VenueComment.objects.filter(venue=pk)
        data = VenueCommentSerializer(venue_comments, many=True).data
        return Response({
            'comments': data,
            'count': int(venue_comments.count()),
        })
