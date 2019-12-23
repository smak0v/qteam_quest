from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from apps.games.models import Game
from apps.games.serializers import GameSerializer
from apps.permissions import IsStaffUserOrReadOnly
from apps.quests.models import Quest, QuestSubscription, QuestComment
from apps.quests.serializers import QuestSerializer, QuestSubscriptionSerializer, QuestCommentSerializer, \
    QuestCommentCreateSerializer, QuestSubscriptionCreateSerializer, QuestUpdateSerializer
from users.models import User
from users.serializers import UserSerializer


class QuestListCreateView(ListCreateAPIView):
    """Class that implements quests create, list view API endpoint"""

    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [
        IsStaffUserOrReadOnly,
    ]


class QuestRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Class that implements quests retrieve, update, destroy view API endpoint"""

    queryset = Quest.objects.all()
    permission_classes = [
        IsStaffUserOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return QuestUpdateSerializer
        return QuestSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        try:
            quest = Quest.objects.get(pk=kwargs.get('pk'))
        except Quest.DoesNotExist:
            return Response({
                'error': 'Quest does not exists!',
            }, status=status.HTTP_404_NOT_FOUND)
        response = {
            'quest': QuestSerializer(quest).data,
        }
        if user.is_authenticated:
            try:
                QuestSubscription.objects.get(user=user, quest=quest)
                response['subscription'] = 'subscribed'
            except QuestSubscription.DoesNotExist:
                response['subscription'] = 'not_subscribed'
        return Response(response, status=status.HTTP_200_OK)


class QuestSubscribersListView(ListCreateAPIView):
    """Class that implements quests subscribers list view API endpoint"""

    queryset = QuestSubscription.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @staticmethod
    def get(request, *args, **kwargs):
        quest_subscriptions = QuestSubscription.objects.filter(quest=kwargs.get('pk'))
        users = list()
        for quest_subscription in quest_subscriptions:
            users.append(User.objects.get(pk=quest_subscription.user.pk))
        data = UserSerializer(users, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class QuestGamesListView(ListAPIView):
    """Class that implements quests`s games list view API endpoint"""

    queryset = QuestSubscription.objects.all()

    @staticmethod
    def get(request, *args, **kwargs):
        games = Game.objects.filter(quest=kwargs.get('pk'))
        data = GameSerializer(games, many=True).data
        return Response({
            'games': data,
            'count': int(games.count()),
        }, status=status.HTTP_200_OK)


class QuestSubscribeCreateView(CreateAPIView):
    """Class that implements quests subscription create view API endpoint"""

    queryset = QuestSubscription.objects.all()
    serializer_class = QuestSubscriptionCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        try:
            user = request.data['user']
        except KeyError:
            raise ValidationError({
                'user': 'Required field!',
            })
        try:
            quest = request.data['quest']
        except KeyError:
            raise ValidationError({
                'quest': 'Required field!',
            })
        if quest != kwargs.get('pk'):
            return Response({
                'message': 'Quest parameter is wrong!',
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            QuestSubscription.objects.get(user=user, quest=quest)
            raise ValidationError({
                'error': 'Quest subscription already exist!',
            })
        except QuestSubscription.DoesNotExist:
            QuestSubscription.objects.create(
                user=User.objects.get(pk=user),
                quest=Quest.objects.get(pk=quest),
            )
            return Response({
                'message': 'Quest subscription created successfully!',
            }, status=status.HTTP_200_OK)


class QuestSubscribeDestroyView(DestroyAPIView):
    """Class that implements quests subscription destroy view API endpoint"""

    queryset = QuestSubscription.objects.all()
    serializer_class = QuestSubscriptionSerializer
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
            quest = request.data['quest']
        except KeyError:
            raise ValidationError({
                'quest': 'Required field!',
            })
        try:
            quest_subscription = QuestSubscription.objects.get(user=user, quest=quest)
        except QuestSubscription.DoesNotExist:
            return Response({
                'message': 'Quest subscription does not exists!',
            }, status=status.HTTP_404_NOT_FOUND)
        quest_subscription.delete()
        return Response({
            'message': 'Quest subscription successfully deleted!',
        }, status=status.HTTP_200_OK)


class QuestCommentListCreateView(ListCreateAPIView):
    """Class that implements quests comment list, create view API endpoint"""

    queryset = QuestComment.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestCommentCreateSerializer
        return QuestCommentSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        quest_comments = QuestComment.objects.filter(quest=kwargs.get('pk'))
        data = QuestCommentSerializer(quest_comments, many=True).data
        return Response({
            'comments': data,
            'count': int(quest_comments.count()),
        }, status=status.HTTP_200_OK)
