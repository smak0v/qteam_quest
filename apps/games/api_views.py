import datetime
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    RetrieveDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.games.models import Game, GameComment
from apps.games.serializers import GameSerializer, GameCommentSerializer, GameCreateUpdateSerializer, \
    GameCommentCreateSerializer, GamePlayerEvaluationCreateSerializer
from apps.permissions import IsStaffUserOrReadOnly
from apps.teams.models import Team, UserInTeam, TemporaryReserve
from apps.teams.serializers import TeamSerializer, UserInTeamSerializer, UserInTeamCreateSerializer, \
    TemporaryReserveSerializer


class GameListCreateView(ListCreateAPIView):
    """Class that implements game list, create views API endpoint"""

    permission_classes = [
        IsStaffUserOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GameCreateUpdateSerializer
        return GameSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        if date is None:
            return Game.objects.all().order_by('timespan')
        try:
            correct_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            return Game.objects.filter(timespan__year=correct_date.year, timespan__month=correct_date.month,
                                       timespan__day=correct_date.day).order_by('timespan')
        except ValueError:
            return Game.objects.all().order_by('timespan')


class GameRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Class that implements game retrieve, update, destroy views API endpoint"""

    queryset = Game.objects.all()
    permission_classes = [
        IsStaffUserOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GameCreateUpdateSerializer
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return GameCreateUpdateSerializer
        return GameSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        try:
            game = Game.objects.get(pk=kwargs.get('pk'))
        except Game.DoesNotExist:
            return Response({
                'error': 'Game does not exists!',
            })
        response = {
            'game': GameSerializer(game).data,
        }
        if user.is_authenticated:
            user_in_team_places_count = UserInTeam.objects.filter(user=user, game=game).count()
            response['seats_purchased_count'] = user_in_team_places_count
            if game.timespan + timezone.timedelta(minutes=game.duration) < timezone.now():
                response['passed'] = True
            else:
                response['passed'] = False
            if response['passed'] or game.cancel:
                response['active'] = False
            else:
                response['active'] = True
            response['reserved_count'] = 0
        return Response(response)


class GameCommentListCreateView(ListCreateAPIView):
    """Class that implements game comment list, create views API endpoint"""

    queryset = GameComment.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GameCommentCreateSerializer
        return GameCommentSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        game_comments = GameComment.objects.filter(game=kwargs.get('pk'))
        data = GameCommentSerializer(game_comments, many=True).data
        return Response({
            'comments': data,
            'count': int(game_comments.count()),
        })


class GameTeamListView(ListAPIView):
    """Class that implements game team view API endpoint"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            team = Team.objects.get(game=kwargs.get('pk'))
            data = TeamSerializer(team).data
            return Response(data)
        except Team.DoesNotExist:
            return Response({
                'error': 'Game does not exist!',
            }, status=status.HTTP_400_BAD_REQUEST)


class GameBookPlacesView(APIView):
    """Class that implements book places for the game view API endpoint"""

    def post(self, request, *args, **kwargs):
        # TODO
        return Response({
            'message': 'Booked successfully!',
        }, status=status.HTTP_200_OK)


class GamePlayersListCreateView(ListCreateAPIView):
    """Class that implements game players list, create view API endpoint"""

    queryset = UserInTeam.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserInTeamCreateSerializer
        return UserInTeamSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            game = Game.objects.get(pk=kwargs.get('pk'))
            users_in_team = UserInTeam.objects.filter(game=game.pk)
            data = UserInTeamSerializer(users_in_team, many=True).data
            return Response(data)
        except Game.DoesNotExist:
            return Response({
                'error': 'Game does not exist!',
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = UserInTeamCreateSerializer(data=request.data)
        if serializer.is_valid():
            # TODO
            return Response({
                'success': 'Successfully created!',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


class GamePlayersRetrieveDestroyView(RetrieveDestroyAPIView):
    """Class that implements game players retrieve, destroy view API endpoint"""

    queryset = UserInTeam.objects.all()
    serializer_class = UserInTeamSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @staticmethod
    def delete(request, *args, **kwargs):
        try:
            user_in_team = UserInTeam.objects.get(game=kwargs.get('pk'), user=kwargs.get('player_pk'))
        except UserInTeam.DoesNotExist:
            return Response({
                'error': 'This player not registered for the game!',
            })
        user_in_team.delete()
        return Response({
            'message': 'Player and all reserved places for this player was deleted successfully!',
        })

    @staticmethod
    def retrieve(request, *args, **kwargs):
        try:
            user_in_team = UserInTeam.objects.get(game=kwargs.get('pk'), user=kwargs.get('player_pk'))
            data = UserInTeamSerializer(user_in_team).data
            return Response(data)
        except UserInTeam.DoesNotExist:
            return Response({
                'error': 'This player not registered for the game!',
            })


class GamePlacesStatusView(APIView):
    """Class that implements game places status view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, pk):
        user = request.user
        try:
            game = Game.objects.get(pk=pk)
            occupied_places_count = TemporaryReserve.objects.filter(game=pk, user=user.pk).count()
            places_in_team_for_game_count = game.max_players_count - (
                    UserInTeam.objects.filter(game=pk).count() + TemporaryReserve.objects.filter(game=pk).count())
            return Response({
                'places_in_team_for_game_count': places_in_team_for_game_count,
                'occupied_places_count': occupied_places_count,
            })
        except Game.DoesNotExist:
            return Response({
                'message': f'Game with id {pk} does not exists!',
            })


class EvaluatePlayerView(CreateAPIView):
    """Class that represents players evaluation after game"""

    serializer_class = GamePlayerEvaluationCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class GameReserveTemporaryPlaceCreateView(CreateAPIView):
    """Class that represents game reserve temporary place create API view endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = TemporaryReserveSerializer(data=self.request.data)
        if serializer.is_valid():
            game = serializer.validated_data.get('game')
            user = serializer.validated_data.get('user')
            if self.request.user != user:
                return Response({
                    'user': 'The user from the request must match the authorized user!',
                }, status=status.HTTP_400_BAD_REQUEST)
            if game.pk != kwargs.get('pk'):
                return Response({
                    'game': 'The game from the request must match the game pk from request url!',
                })
            if game.timespan + timezone.timedelta(minutes=game.duration) < timezone.now():
                return Response({
                    'error': 'Unable to register for the past game!',
                }, status=status.HTTP_400_BAD_REQUEST)
            if game.players_count < game.max_players_count:
                place = TemporaryReserve.objects.create(game=game, user=user)
            else:
                return Response({
                    'error': 'Not enough places in this game!',
                }, status=status.HTTP_400_BAD_REQUEST)
            send_game_status_message_to_socket(game, self.request.user)
            return Response({
                'reserved_place': TemporaryReserveSerializer(place).data,
                'message': 'Successfully created!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameReserveTemporaryPlaceDestroyView(DestroyAPIView):
    """Class that represents game reserve temporary place destroy API view endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        try:
            game = Game.objects.get(pk=kwargs.get('pk'))
        except Game.DoesNotExist:
            return Response({
                'game': 'Game does not exist!',
            }, status=status.HTTP_400_BAD_REQUEST)
        if TemporaryReserve.objects.filter(user=user.pk, game=game.pk).count() < 1:
            return Response({
                'error': 'User has no reserved places for this game!',
            }, status=status.HTTP_400_BAD_REQUEST)
        place = TemporaryReserve.objects.filter(user=user.pk, game=game.pk).first()
        place.delete()
        send_game_status_message_to_socket(game, user)
        return Response({
            'message': 'Successfully deleted!'
        }, status=status.HTTP_200_OK)


def send_game_status_message_to_socket(game, user):
    occupied_places_count = TemporaryReserve.objects.filter(game=game.pk, user=user.pk).count()
    places_in_team_for_game_count = game.max_players_count - (
            UserInTeam.objects.filter(game=game.pk).count() + TemporaryReserve.objects.filter(game=game.pk).count())
    obj = {
        'places_in_team_for_game_count': places_in_team_for_game_count,
        'occupied_places_count': occupied_places_count,
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(game.pk),
        {
            'type': 'game_message',
            'message': json.dumps(obj),
        },
    )
