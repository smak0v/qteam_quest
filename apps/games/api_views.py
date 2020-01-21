import datetime
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    RetrieveDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex_checkout import Configuration
from yandex_checkout import Payment

from apps.coupons.models import Coupon
from apps.coupons.serializers import CouponCheckSerializer
from apps.games.models import Game, GameComment, GamePayment
from apps.games.serializers import GameSerializer, GameCommentSerializer, GameCreateUpdateSerializer, \
    GameCommentCreateSerializer, GamePlayerEvaluationCreateSerializer
from apps.permissions import IsStaffUserOrReadOnly
from apps.teams.models import Team, UserInTeam, TemporaryReserve
from apps.teams.serializers import TeamSerializer, UserInTeamSerializer, TemporaryReserveSerializer


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


class GameReservedPlacesInfoView(APIView):
    """Class that implements game reserved places info for user view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, *args, **kwargs):
        user = self.request.user
        pk = kwargs.get('pk')
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({
                'error': f'Game with id {pk} does not exist!',
            }, status=status.HTTP_400_BAD_REQUEST)
        occupied_places_count = TemporaryReserve.objects.filter(game=pk, user=user.pk).count()
        summa = game.price * occupied_places_count
        return Response({
            'occupied_places_count': occupied_places_count,
            'summa': summa,
            'is_coupon': True,
        }, status=status.HTTP_200_OK)


class GamePaymentTokenView(APIView):
    """Class that implements game payment token view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        Configuration.account_id = settings.YANDEX_ACCOUNT_ID
        Configuration.secret_key = settings.YANDEX_SECRET_KEY
        user = self.request.user
        serializer = CouponCheckSerializer(data=self.request.data)
        if serializer.is_valid():
            if serializer.validated_data['game_id'] != kwargs.get('pk'):
                return Response({
                    'game_id': 'Must be equal to game id from url!',
                }, status=status.HTTP_400_BAD_REQUEST)
            coupon = Coupon.objects.get(code=serializer.validated_data.get('code'))
            reserved_places_count = TemporaryReserve.objects.filter(user=user.pk, game=kwargs.get('pk')).count()
            if reserved_places_count == 0:
                return Response({
                    'error': 'You have no reserved seats for this game or payment time exceeded 5 minutes. Try again!',
                }, status=status.HTTP_400_BAD_REQUEST)
            game = Game.objects.get(pk=serializer.validated_data['game_id'])
            if coupon.type == 'INDIVIDUAL':
                if coupon.user != user:
                    return Response({
                        'error': 'Invalid user for this INDIVIDUAL coupon!',
                    }, status=status.HTTP_400_BAD_REQUEST)
                summa = self.apply_individual_discount(coupon, game, reserved_places_count)
            else:
                summa = self.apply_general_discount(coupon, game, reserved_places_count)
            payment = Payment.create({
                'amount': {
                    'value': str(summa),
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': 'embedded',
                },
                'capture': True,
                'description': 'Description',
            })
            GamePayment.objects.create(
                identifier=payment.id,
                user=user,
                game=game,
                coupon=coupon,
                summa=round(game.price * reserved_places_count, 2),
                discount=round(coupon.discount, 2),
                discount_units=coupon.units,
                summa_with_discount=round(summa, 2),
                currency='RUB',
                places_count=reserved_places_count,
            )
            return Response({
                'yandex_token': payment.id,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def apply_general_discount(coupon, game, reserved_places_count):
        summa = game.price * reserved_places_count
        if coupon.units == 'RUB':
            summa -= coupon.discount
        elif coupon.units == 'PERCENT':
            summa -= (game.price * coupon.discount) / 100
        return round(summa, 2)

    @staticmethod
    def apply_individual_discount(coupon, game, reserved_places_count):
        summa = game.price * reserved_places_count
        if coupon.units == 'RUB':
            summa -= coupon.discount
        elif coupon.units == 'PERCENT':
            summa -= (game.price * coupon.discount) / 100
        return round(summa, 2)


class GamePlayersListView(ListAPIView):
    """Class that implements game players list view API endpoint"""

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


class GamePlayersRetrieveView(RetrieveDestroyAPIView):
    """Class that implements game players retrieve view API endpoint"""

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
            temporary_reserve_places_count = TemporaryReserve.objects.filter(game=game.pk).count()
            if game.players_count + temporary_reserve_places_count < game.max_players_count:
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
        'user_id': user.pk,
        'game_id': game.pk,
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
