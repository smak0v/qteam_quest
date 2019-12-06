import random
import re

import requests
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.games.models import Game
from apps.games.serializers import GameSerializer
from apps.teams.models import UserInTeam
from apps.venues.models import VenueSubscription
from apps.venues.serializers import VenueSubscriptionSerializer
from korobka_games.utils import get_env_value
from users.models import User, UserSubscription
from users.serializers import UserSerializer, UserSubscriptionSerializer, UserSubscriptionCreateSerializer, \
    UserChangePasswordSerializer, UpdateUserProfileSerializer, UserAuthTokenSerializer, UserChangePhoneNumberSerializer, \
    UserChangePhoneNumberConfirmSerializer


class UserListView(ListAPIView):
    """Class that implements user list view API endpoint"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterView(RegisterView):
    """Class that implements user register view API endpoint"""

    queryset = User.objects.all()


class UserChangePasswordView(UpdateAPIView):
    """Class that implements user change password view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = UserChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({
                    'old_password': 'Wrong password!',
                }, status=status.HTTP_400_BAD_REQUEST)
            if serializer.data.get('new_password_1') != serializer.data.get('new_password_2'):
                return Response({
                    'error': 'Passwords must be equals!',
                }, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password_2'))
            user.save()
            return Response({
                'success': 'Password was changed successfully!',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """Class that implements user retrieve, update, destroy view API endpoint"""

    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    parser_classes = [
        MultiPartParser,
        JSONParser,
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return UserSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateUserProfileSerializer

    def retrieve(self, request, pk):
        try:
            user_for_response = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                'error': 'User does not exist!',
            }, status=status.HTTP_404_NOT_FOUND)
        user = {
            'id': user_for_response.id,
            'username': user_for_response.username,
            'first_name': user_for_response.first_name,
            'last_name': user_for_response.last_name,
            'location': user_for_response.location,
            'gender': user_for_response.gender,
            'nationality': user_for_response.nationality,
            'favourite_position': user_for_response.favourite_position,
            'active': user_for_response.active,
            'staff': user_for_response.staff,
            'admin': user_for_response.admin,
            'reliability': user_for_response.reliability,
        }
        try:
            user['profile_image'] = user_for_response.profile_image.url
        except ValueError:
            user['profile_image'] = user_for_response.get_profile_image()
        if isinstance(self.request.user, AnonymousUser):
            return Response({
                'user': user,
            }, status=status.HTTP_200_OK)
        if self.request.user.is_authenticated:
            if pk != self.request.user.pk:
                try:
                    user_user_subscription = UserSubscription.objects.get(user=user_for_response,
                                                                          subscriber=self.request.user)
                    return Response({
                        'user': user,
                        'subscription': 'subscribed',
                    }, status=status.HTTP_200_OK)
                except UserSubscription.DoesNotExist:
                    return Response({
                        'user': user,
                        'subscription': 'not_subscribed',
                    }, status=status.HTTP_200_OK)
            else:
                user['email'] = user_for_response.email
                user['phone'] = user_for_response.phone
                user['is_active_phone'] = user_for_response.is_active_phone
                return Response({
                    'user': user,
                }, status=status.HTTP_200_OK)

    def update(self, request, pk):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            usr = None
            try:
                usr = User.objects.get(username=serializer.validated_data.get('username'))
            except User.DoesNotExist:
                user.username = serializer.validated_data.get('username', user.username)
            if usr is not None:
                if usr != user:
                    return Response({
                        'error': 'User with this username already exists!',
                    }, status=status.HTTP_400_BAD_REQUEST)
            usr = None
            try:
                usr = User.objects.get(email=serializer.validated_data.get('email'))
            except User.DoesNotExist:
                user.email = serializer.validated_data.get('email', user.email)
            if usr is not None:
                if usr != user:
                    return Response({
                        'error': 'User with this email already exists!',
                    }, status=status.HTTP_400_BAD_REQUEST)
            user.profile_image = serializer.validated_data.get('profile_image', None)
            user.first_name = serializer.validated_data.get('first_name', user.first_name)
            user.last_name = serializer.validated_data.get('last_name', user.last_name)
            user.location = serializer.validated_data.get('location', user.location)
            user.gender = serializer.validated_data.get('gender', user.gender)
            user.nationality = serializer.validated_data.get('nationality', user.nationality)
            user.favourite_position = serializer.validated_data.get('favourite_position', user.favourite_position)
            user.save()
            return Response({
                'success': 'User profile updated successfully!',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({
                'message': 'User with {} primary key was deleted successfully!'.format(pk),
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'message': 'User with {} primary key does not exists!'.format(pk),
            }, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    """Class that implements user profile view API endpoint"""

    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    parser_classes = [
        JSONParser,
    ]

    @staticmethod
    def post(request):
        serialzer = UserAuthTokenSerializer(data=request.data)
        if serialzer.is_valid():
            try:
                token = Token.objects.get(key=request.data['token'])
                user = User.objects.get(username=token.user)
            except Token.DoesNotExist:
                return Response({
                    'error': 'User with this token does not exist!',
                }, status=status.HTTP_404_NOT_FOUND)
            return Response({
                'user': UserSerializer(user).data,
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Token is required!',
        }, status=status.HTTP_400_BAD_REQUEST)


class UserVenueSubscriptionsListView(APIView):
    """Class that implements user venue subscriptions list view API endpoint"""

    @staticmethod
    def get(request, pk):
        venue_subscriptions = VenueSubscription.objects.filter(user=pk)
        data = VenueSubscriptionSerializer(venue_subscriptions, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UserSubscribersListView(ListAPIView):
    """Class that implements user subscribers list view API endpoint """

    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, pk):
        try:
            user_subscribers = UserSubscription.objects.filter(user=pk)
            data = UserSubscriptionSerializer(user_subscribers, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except UserSubscription.DoesNotExist:
            return Response({
                'message': 'No subscribers!',
            }, status=status.HTTP_404_NOT_FOUND)


class UserSubscriptionsListView(ListAPIView):
    """Class that implements user subscriptions list view API endpoint """

    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, pk):
        try:
            user_subscriptions = UserSubscription.objects.filter(subscriber=pk)
            data = UserSubscriptionSerializer(user_subscriptions, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except UserSubscription.DoesNotExist:
            return Response({
                'message': 'No subscriptions!',
            }, status=status.HTTP_404_NOT_FOUND)


class UserSubscribeView(CreateAPIView):
    """Class that implements user subscription create view API endpoint"""

    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class UserUnsubscribeView(DestroyAPIView):
    """Class that implements user subscription delete view API endpoint"""

    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def destroy(request, pk):
        try:
            user_subscription = UserSubscription.objects.get(user=request.POST['user'],
                                                             subscriber=request.POST['subscriber'])
            user_subscription.delete()
            return Response({
                'message': 'Successfully deleted!',
            }, status=status.HTTP_200_OK)
        except UserSubscription.DoesNotExist:
            return Response({
                'message': 'User subscription does not exists!',
            }, status=status.HTTP_404_NOT_FOUND)


class UserGamesListView(ListAPIView):
    """Class that implements user games list view API endpoint"""

    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, pk):
        user_in_teams = UserInTeam.objects.filter(user=pk)
        user_games = list()
        for user_in_team in user_in_teams:
            user_games.append(Game.objects.get(pk=user_in_team.team.game))
        data = GameSerializer(user_games, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UserPastGamesListView(ListAPIView):
    """Class that implements user past games list view API endpoint"""

    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, pk):
        user_in_teams = UserInTeam.objects.filter(user=pk)
        user_games = list()
        now = timezone.now()
        for user_in_team in user_in_teams:
            user_games.append(Game.objects.get(timespan__lt=now).order_by('-timespan'))
        data = GameSerializer(user_games, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UserFutureGamesListView(ListAPIView):
    """Class that implements user future games list view API endpoint"""

    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, pk):
        user_in_teams = UserInTeam.objects.filter(user=pk)
        user_games = list()
        now = timezone.now()
        for user_in_team in user_in_teams:
            user_games.append(Game.objects.get(timespan__gte=now).order_by('timespan'))
        data = GameSerializer(user_games, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ChangePhoneView(APIView):
    """Change user phone view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]
    parser_classes = [
        JSONParser,
    ]

    @staticmethod
    def post(request, pk):
        serializer = UserChangePhoneNumberSerializer(data=request.data)
        prostor_sms_api_login = get_env_value('PROSTOR_SMS_API_LOGIN')
        prostor_sms_api_password = get_env_value('PROSTOR_SMS_API_PASSWORD')
        user = User.objects.get(pk=pk)
        if serializer.is_valid():
            phone = request.data['phone']
            phone_activation_code = random.randint(10000, 99999)
            if re.match('^((\+38|\+7|\+8)+([0-9]){10})$', phone):
                user.phone = phone
                user.phone_activation_code = phone_activation_code
                user.save()
                sms_text = f'Подтвердите добавление или смену номера телефона.\nКод: {phone_activation_code}'
                send_sms_url = f'http://{prostor_sms_api_login}:{prostor_sms_api_password}@api.prostor-sms.ru/send/' \
                               f'?phone={phone}&text={sms_text}'
                response = requests.get(url=send_sms_url)
                if response.content == b'not enough credits':
                    return Response({
                        'message': 'Not enough credits in Prostor SMS account!',
                    }, status=status.HTTP_400_BAD_REQUEST)
                if response.content == b'invalid mobile phone':
                    return Response({
                        'message': 'Invalid mobile phone!',
                    }, status=status.HTTP_400_BAD_REQUEST)
                if response.content == b'text is empty':
                    return Response({
                        'message': 'Text is empty!',
                    }, status=status.HTTP_400_BAD_REQUEST)
                if response.content == b'accepted':
                    return Response({
                        'message': 'Phone successfully changed!',
                    }, status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    'message': f'Activation code was sent by number {phone}',
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'Number is not in russian number format!',
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': 'Phone field is required!',
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePhoneConfirmView(APIView):
    """Change user phone confirm view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]
    parser_classes = [
        JSONParser,
    ]

    @staticmethod
    def post(request, pk):
        serializer = UserChangePhoneNumberConfirmSerializer(data=request.data)
        user = User.objects.get(pk=pk)
        if serializer.is_valid():
            sms_code = request.data['sms_code']
            try:
                if int(sms_code) == user.phone_activation_code:
                    user.is_active_phone = True
                    user.save()
                    return Response({
                        'message': 'Phone successfully activated!',
                    }, status=status.HTTP_200_OK)
                return Response({
                    'message': 'Not valid activation code! Try again!',
                }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'message': 'Not valid activation code! Try again!',
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'sms_code': 'SMS code is required!',
        }, status=status.HTTP_400_BAD_REQUEST)
