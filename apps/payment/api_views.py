from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.games.models import Game
from apps.payment.serializers import PaymentSuccessSerializer
from apps.teams.models import UserInTeam, TemporaryReserve, Team


class PaymentSuccessView(APIView):
    """Class that implements payment success view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, *args, **kwargs):
        user = self.request.user
        serializer = PaymentSuccessSerializer(data=self.request.data)
        if serializer.is_valid():
            game_id = serializer.validated_data['game_id']
            reserved_places = TemporaryReserve.objects.filter(game=game_id, user=user.pk)
            reserved_places_count = reserved_places.count()
            if reserved_places_count == 0:
                return Response({
                    'error': 'You have no reserved seats for this game or payment time exceeded 5 minutes. Try again!',
                }, status=status.HTTP_400_BAD_REQUEST)
            user_in_team_places_count = UserInTeam.objects.filter(game=game_id, user=user.pk).count()
            game = Game.objects.get(pk=game_id)
            team = Team.objects.get(game=game)
            if user_in_team_places_count != 0:
                for _ in range(reserved_places_count):
                    self.create_user_in_team(game, team, user, True)
            else:
                self.create_user_in_team(game, team, user)
                for _ in range(reserved_places_count - 1):
                    self.create_user_in_team(game, team, user, True)
            for reserved_place in reserved_places:
                reserved_place.delete()
            return Response({
                'success': 'Payment success!',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create_user_in_team(game, team, user, title=False):
        if title:
            text_title = user.username + '`s friend'
        else:
            text_title = user.username
        user_in_team = UserInTeam.objects.create(
            game=game,
            team=team,
            user=user,
            title=text_title,
        )
        game.players_count += 1
        game.save()
