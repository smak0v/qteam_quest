from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex_checkout import Payment, Configuration

from apps.games.models import Game, GamePayment
from apps.payment.serializers import PaymentSaveSerializer
from apps.teams.models import UserInTeam, TemporaryReserve, Team


class PaymentSaveView(APIView):
    """Class that implements payment save view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, *args, **kwargs):
        Configuration.account_id = settings.YANDEX_ACCOUNT_ID
        Configuration.secret_key = settings.YANDEX_SECRET_KEY
        user = self.request.user
        serializer = PaymentSaveSerializer(data=self.request.data)
        if serializer.is_valid():
            payment = Payment.find_one(serializer.validated_data['payment_id'])
            game_payment = GamePayment.objects.get(identifier=serializer.validated_data['payment_id'])
            if payment.status == 'CANCELED':
                game_payment.status = 'CANCELED'
                game_payment.cancel_message = payment.cancellation_details.party + ': ' + payment.cancellation_details.reason
                game_payment.save()
                return Response({
                    'message': 'Payment was canceled!',
                    'party': payment.cancellation_details.party,
                    'reason': payment.cancellation_details.reason,
                }, status=status.HTTP_200_OK)
            game_id = serializer.validated_data['game_id']
            reserved_places = TemporaryReserve.objects.filter(game=game_id, user=user.pk)
            reserved_places_count = reserved_places.count()
            if reserved_places_count == 0:
                return Response({
                    'error': 'You have no reserved seats for this game or payment time exceeded 10 minutes. Try again!',
                }, status=status.HTTP_400_BAD_REQUEST)
            user_in_team_places_count = UserInTeam.objects.filter(game=game_id, user=user.pk).count()
            game = Game.objects.get(pk=game_id)
            team = Team.objects.get(game=game)
            if user_in_team_places_count != 0:
                for _ in range(reserved_places_count):
                    self.create_user_in_team(game, team, user, game_payment, True)
            else:
                self.create_user_in_team(game, team, user, game_payment)
                for _ in range(reserved_places_count - 1):
                    self.create_user_in_team(game, team, user, game_payment, True)
            for reserved_place in reserved_places:
                reserved_place.delete()
            return Response({
                'message': 'Places was registered successfully!',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create_user_in_team(game, team, user, game_payment, title=False):
        if title:
            text_title = user.username + '`s friend'
        else:
            text_title = user.username
        user_in_team = UserInTeam.objects.create(
            game=game,
            team=team,
            user=user,
            title=text_title,
            payment=game_payment,
        )
        game.players_count += 1
        game.save()


class YandexNotificationsView(APIView):
    """Class that implements yandex notifications view API endpoint (for Yandex webhooks)"""

    def post(self, *args, **kwargs):
        data = request.data
        if data['event'] == 'payment.waiting_for_capture':
            self.process_payment_waiting_fo_capture(data)
        elif data['event'] == 'payment.succeeded':
            self.process_payment_succeeded(data)
        elif data['event'] == 'payment.canceled':
            self.process_payment_canceled(data)
        elif data['event'] == 'refund.succeeded':
            self.process_refund_succeeded(data)
        return Response({}, status=status.HTTP_200_OK)

    def process_payment_succeeded(self, data):
        self.set_payment_status(data['object']['id'], 'SUCCEEDED')

    def process_payment_canceled(self, data):
        res = data['object']['cancellation_details']['party'] + ': ' + data['object']['cancellation_details']['reason']
        self.set_payment_status(data['object']['id'], 'CANCELED', res)
        self.delete_registrations_and_reserves(data['object']['id'])

    def process_payment_waiting_fo_capture(self, data):
        self.set_payment_status(data['object']['id'], 'WAITING_FOR_CAPTURE')

    @staticmethod
    def process_refund_succeeded(data):
        pass

    @staticmethod
    def set_payment_status(identifier, payment_status, reason=None):
        try:
            game_payment = GamePayment.objects.get(identifier=identifier)
            game_payment.status = payment_status
            if reason:
                game_payment.cancel_message = reason
            game_payment.save()
        except GamePayment.DoesNotExist:
            pass

    @staticmethod
    def delete_registrations_and_reserves(identifier):
        try:
            game_payment = GamePayment.objects.get(identifier=identifier)
            users_in_team_by_payment = UserInTeam.objects.filter(payment=game_payment.pk)
            for user in users_in_team_by_payment:
                user.delete()
        except GamePayment.DoesNotExist:
            pass
