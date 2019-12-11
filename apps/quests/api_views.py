import datetime

from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quests.models import Game, GameComment
from apps.quests.serializers import GameSerializer, GameCommentSerializer, GameCreateUpdateSerializer, \
    GameCommentCreateUpdateSerializer, GamePlayerEvaluationCreateSerializer
from apps.teams.models import Team, UserInTeam, ReservedPlaceInTeam
from apps.teams.serializers import TeamSerializer, UserInTeamSerializer, ReservedPlaceInTeamSerializer, \
    UserInTeamCreateUpdateSerializer, ReservedPlaceInTeamCreateUpdateSerializer


class GameListCreateView(ListCreateAPIView):
    """Class that implements game list, create views API endpoint"""

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'UPDATE':
            return GameCreateUpdateSerializer
        return GameSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        if date is None:
            return Game.objects.filter(cancel=False).order_by('timespan')
        try:
            correct_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            return Game.objects.filter(timespan__year=correct_date.year, timespan__month=correct_date.month,
                                       timespan__day=correct_date.day, cancel=False).order_by('timespan')
        except ValueError:
            return Game.objects.filter(cancel=False).order_by('timespan')


class GameRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Class that implements game retrieve, update, destroy views API endpoint"""

    queryset = Game.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return GameCreateUpdateSerializer
        return GameSerializer

    def retrieve(self, request, pk):
        user = self.request.user
        try:
            game = Game.objects.get(pk=pk, cancel=False)
        except Game.DoesNotExist:
            return Response({
                'error': 'Game does not exists!',
            })
        response = {
            'game': GameSerializer(game).data,
        }
        if user.is_authenticated:
            try:
                user_in_team = UserInTeam.objects.get(user=user, game=game)
                reserved_places_count_by_user = ReservedPlaceInTeam.objects.filter(user=user, game=game).count()
                response['seats_purchased_count'] = 1 + reserved_places_count_by_user
            except UserInTeam.DoesNotExist:
                response['seats_purchased_count'] = 0
            if game.timespan + timezone.timedelta(minutes=game.duration) < timezone.now():
                response['passed'] = True
            else:
                response['passed'] = False
            reserved_places_count = ReservedPlaceInTeam.objects.filter(game=game).count()
            if reserved_places_count + 1 < int(game.a_side_players_count) * 2:
                if response['passed']:
                    response['active'] = False
                else:
                    response['active'] = True
        return Response(response)


class GameCommentListCreateView(ListCreateAPIView):
    """Class that implements game comment list, create views API endpoint"""

    queryset = GameComment.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'UPDATE':
            return GameCommentCreateUpdateSerializer
        return GameCommentSerializer

    @staticmethod
    def get(request, pk):
        game_comments = GameComment.objects.filter(game=pk)
        data = GameCommentSerializer(game_comments, many=True).data
        return Response({
            'comments': data,
            'count': int(game_comments.count()),
        })


class GameTeamsListView(ListAPIView):
    """Class that implements game teams list view API endpoint"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @staticmethod
    def get(request, pk):
        teams = Team.objects.filter(game=pk)
        data = TeamSerializer(teams, many=True).data
        return Response(data)


class GamePlayersListCreateView(ListCreateAPIView):
    """Class that implements game players list view API endpoint"""

    queryset = UserInTeam.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'UPDATE':
            return UserInTeamCreateUpdateSerializer
        return UserInTeamSerializer

    @staticmethod
    def get(request, pk):
        team = request.query_params.get('team')
        if team is None:
            users_in_team = UserInTeam.objects.filter(game=pk)
            data = UserInTeamSerializer(users_in_team, many=True).data
            return Response(data)
        users_in_team = None
        if team == 'black':
            users_in_team = UserInTeam.objects.filter(team=Team.objects.get(name='Черные майки', game=pk))
            data = UserInTeamSerializer(users_in_team, many=True).data
            return Response(data)
        elif team == 'white':
            users_in_team = UserInTeam.objects.filter(team=Team.objects.get(name='Белые майки', game=pk))
            data = UserInTeamSerializer(users_in_team, many=True).data
            return Response(data)
        else:
            return Response({
                'message': 'Wrong team parameter!',
            })


class GamePlayersRetrieveDestroyView(RetrieveDestroyAPIView):
    """Class that implements game players retrieve, destroy view API endpoint"""

    queryset = UserInTeam.objects.all()
    serializer_class = UserInTeamSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @staticmethod
    def delete(request, pk, player_pk):
        try:
            user_in_team = UserInTeam.objects.get(game=pk, user=player_pk)
        except UserInTeam.DoesNotExist:
            return Response({
                'message': 'This player not registered for the game!',
            })
        reserved_places_by_user = ReservedPlaceInTeam.objects.filter(user=player_pk, game=pk)
        for reserved_place_by_user in reserved_places_by_user:
            reserved_place_by_user.delete()
        user_in_team.delete()
        return Response({
            'message': 'Player and all reserved places for this player was deleted successfully!',
        })

    @staticmethod
    def retrieve(request, pk, player_pk):
        try:
            user_in_team = UserInTeam.objects.get(game=pk, user=player_pk)
            data = UserInTeamSerializer(user_in_team).data
            return Response(data)
        except UserInTeam.DoesNotExist:
            return Response({
                'message': 'This player not registered for the game!',
            })


class GameReservedPlacesListCreateView(ListCreateAPIView):
    """Class that implements game reserved places list view API endpoint"""

    queryset = ReservedPlaceInTeam.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'UPDATE':
            return ReservedPlaceInTeamCreateUpdateSerializer
        return ReservedPlaceInTeamSerializer

    @staticmethod
    def get(request, pk):
        team = request.query_params.get('team')
        if team is None:
            reserved_places = ReservedPlaceInTeam.objects.filter(game=pk)
            data = ReservedPlaceInTeamSerializer(reserved_places, many=True).data
            return Response(data)
        reserved_places_in_team = None
        if team == 'black':
            reserved_places_in_team = ReservedPlaceInTeam.objects.filter(
                team=Team.objects.get(name='Черные майки', game=pk))
            data = ReservedPlaceInTeamSerializer(reserved_places_in_team, many=True).data
            return Response(data)
        elif team == 'white':
            reserved_places_in_team = ReservedPlaceInTeam.objects.filter(
                team=Team.objects.get(name='Белые майки', game=pk))
            data = ReservedPlaceInTeamSerializer(reserved_places_in_team, many=True).data
            return Response(data)
        else:
            return Response({
                'message': 'Wrong team parameter!',
            })


class GameReservedPlacesRetrieveDestroyView(RetrieveDestroyAPIView):
    """Class that implements game reserved places retrieve, delete API view endpoint"""

    queryset = ReservedPlaceInTeam.objects.all()
    serializer_class = ReservedPlaceInTeamSerializer

    @staticmethod
    def delete(request, pk, reserve_user_pk):
        count = request.query_params.get('count')
        reserved_places = ReservedPlaceInTeam.objects.filter(game=pk, user=reserve_user_pk)
        if count is None:
            return Response({
                'message': 'Pass the count parameter to the request!',
            })
        if count == 'all':
            for reserved_place in reserved_places:
                reserved_place.delete()
            return Response({
                'message': 'All reserved places was deleted successfully!',
            })
        else:
            reserved_places_count = len(reserved_places)
            try:
                if int(count) > reserved_places_count:
                    return Response({
                        'message': 'You are trying to delete too many reserved places!',
                    })
                else:
                    for i in range(int(count)):
                        reserved_places[i].delete()
                    return Response({
                        'message': '{} reserved places was deleted successfully!'.format(count)
                    })
            except ValueError:
                return Response({
                    'message': 'Pass the count parameter to the request!',
                })

    @staticmethod
    def retrieve(request, pk, reserve_user_pk):
        reserved_places = ReservedPlaceInTeam.objects.filter(game=pk, user=reserve_user_pk)
        if len(reserved_places) == 0:
            return Response({
                'message': 'No reserved places for this player!',
            })
        data = ReservedPlaceInTeamSerializer(reserved_places, many=True).data
        return Response(data)


class GamePlacesStatusView(APIView):
    """Class that implements game places status view API endpoint"""

    @staticmethod
    def get(request, pk):
        try:
            places_in_teams_count = int(Game.objects.get(pk=pk).a_side_players_count) * 2
            users_in_teams_for_game_count = 0
            reserved_places_in_teams_for_game_count = 0
            try:
                users_in_teams_for_game_count = int(UserInTeam.objects.filter(game=pk).count())
            except UserInTeam.DoesNotExist:
                users_in_teams_for_game_count = 0
            try:
                reserved_places_in_teams_for_game_count = int(ReservedPlaceInTeam.objects.filter(game=pk).count())
            except ReservedPlaceInTeam.DoesNotExist:
                reserved_places_in_teams_for_game_count = 0
            return Response({
                'places_in_teams_for_game_count': places_in_teams_count,
                'occupied_places_count': users_in_teams_for_game_count + reserved_places_in_teams_for_game_count,
            })
        except Game.DoesNotExist:
            return Response({
                'message': 'Game with id {} does not exists!'.format(pk),
            })


class EvaluatePlayerView(CreateAPIView):
    """Class that represents players evaluation after game"""

    serializer_class = GamePlayerEvaluationCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]
