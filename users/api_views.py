import random
import re

import requests
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quests.models import Game
from apps.quests.serializers import GameSerializer
from apps.teams.models import UserInTeam
from apps.venues.models import VenueSubscription
from apps.venues.serializers import VenueSubscriptionSerializer
from qteam_quest.utils import get_env_value
from users.models import User, UserSubscription
from users.serializers import UserSerializer, UserSubscriptionSerializer, UserSubscriptionCreateSerializer, \
    UserChangePasswordSerializer, UpdateUserProfileSerializer, UserAuthTokenSerializer, \
    UserChangePhoneNumberSerializer, UserChangePhoneNumberConfirmSerializer, UserLoginSerializer, \
    UserLoginConfirmSerializer
from users.utils import send_sms_code


class UserListView(ListAPIView):
    """Class that implements user list view API endpoint"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    """Class that implements user login view API endpoint"""

    @staticmethod
    def post(request, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            if re.match('^((\+38|\+7|\+8)+([0-9]){10})$', phone):
                one_time_password = random.randint(10000, 99999)
                try:
                    user = User.objects.get(phone=phone)
                    sms_text = f'Войдите, используя код: {one_time_password}'
                except User.DoesNotExist:
                    user = User.objects.create(phone=phone)
                    Token.objects.create(user=user)
                    sms_text = f'Вы были успешно зарегестрированы!\nВойдите, используя код: {one_time_password}'
                user.set_password(one_time_password)
                user.save()
                send_sms_code(phone, sms_text)
                return Response({
                    'success': f'Code was sent by number {phone}.',
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Number is not in russian number format!',
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': 'Phone is required!',
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginConfirmView(APIView):
    """Class that implements user login confirm view API endpoint"""

    @staticmethod
    def post(request, **kwargs):
        serializer = UserLoginConfirmSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            sms_code = serializer.validated_data.get('sms_code')
            if re.match('^((\+38|\+7|\+8)+([0-9]){10})$', phone):
                user = authenticate(username=phone, password=sms_code)
                if not user:
                    return Response({
                        'error': 'User with this credentials does not exist!',
                    }, status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    'token': Token.objects.get(user=user).key,
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Number is not in russian number format!',
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': 'Phone and SMS_code are required!',
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """Class that implements user logout view API endpoint"""

    @staticmethod
    def get(request, **kwargs):
        logout(request=request)
        return Response({
            'success': 'Logged out successfully!',
        })


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

    def retrieve(self, request, *args, **kwargs):
        try:
            user_for_response = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return Response({
                'error': 'User does not exist!',
            }, status=status.HTTP_404_NOT_FOUND)
        user = {
            'id': user_for_response.id,
            'phone': user_for_response.phone,
            'is_active_phone': user_for_response.is_active_phone,
            'username': user_for_response.username,
            'first_name': user_for_response.first_name,
            'last_name': user_for_response.last_name,
            'birthday_date': user_for_response.birthday_date,
            'gender': user_for_response.gender,
            'location': user_for_response.location,
            'about': user_for_response.about,
            'reliability': user_for_response.reliability,
            'active': user_for_response.active,
            'staff': user_for_response.staff,
            'admin': user_for_response.admin,
            'profile_image': user_for_response.get_profile_image(),
        }
        if isinstance(self.request.user, AnonymousUser):
            return Response({
                'user': user,
            }, status=status.HTTP_200_OK)
        if self.request.user.is_authenticated:
            if kwargs.get('pk') != self.request.user.pk:
                try:
                    UserSubscription.objects.filter(user=user_for_response, subscriber=self.request.user).first()
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
                return Response({
                    'user': user,
                }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        request_user = request.user
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return Response({
                'error': 'User does not exist!',
            })
        if user != request_user:
            return Response({
                'error': 'Invalid authentication!',
            })
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            usr = None
            # if not re.match('^((\+38|\+7|\+8)+([0-9]){10})$', serializer.validated_data.get('phone')):
            #     return Response({
            #         'phone': 'Must be in russian format number!',
            #     })
            # try:
            #     usr = User.objects.get(phone=serializer.validated_data.get('phone'))
            # except User.DoesNotExist:
            #     request_user.phone = serializer.validated_data.get('phone', request_user.phone)
            # if usr is not None:
            #     if usr != user:
            #         return Response({
            #             'error': 'User with this phone already exists!',
            #         }, status=status.HTTP_400_BAD_REQUEST)
            request_user.username = serializer.validated_data.get('username', request_user.username)
            request_user.first_name = serializer.validated_data.get('first_name', request_user.first_name)
            request_user.last_name = serializer.validated_data.get('last_name', request_user.last_name)
            request_user.birthday_date = serializer.validated_data.get('birthday_date', request_user.birthday_date)
            request_user.location = serializer.validated_data.get('location', request_user.location)
            request_user.gender = serializer.validated_data.get('gender', request_user.gender)
            request_user.profile_image = serializer.validated_data.get('profile_image', None)
            request_user.about = serializer.validated_data.get('about', request_user.about)
            request_user.save()
            return Response({
                'success': 'User profile updated successfully!',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def destroy(request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
            if request.user == user:
                user.delete()
                return Response({
                    'message': 'User was deleted successfully!'.format(kwargs.get('pk')),
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'Invalid authentication!',
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'message': 'User does not exist!',
            }, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    """Class that implements user profile view API endpoint"""

    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def post(request, **kwargs):
        serializer = UserAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            if request.META.get('HTTP_AUTHORIZATION').split(' ')[1] != serializer.validated_data.get('token'):
                return Response({
                    'error': 'Invalid authorization token!',
                })
            try:
                token = Token.objects.get(key=serializer.validated_data.get('token'))
                user = User.objects.get(phone=token.user)
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

    permission_classes = [
        IsAuthenticated,
    ]

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
    """Class that implements user quests list view API endpoint"""

    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, *args, **kwargs):
        user_in_teams = UserInTeam.objects.filter(user=kwargs.get('pk'))
        user_games = list()
        for user_in_team in user_in_teams:
            user_games.append(Game.objects.get(pk=user_in_team.team.game.pk))
        data = GameSerializer(user_games, many=True).data
        return Response({
            'games': data,
        }, status=status.HTTP_200_OK)


class UserPastGamesListView(ListAPIView):
    """Class that implements user past quests list view API endpoint"""

    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, *args, **kwargs):
        user_in_teams = UserInTeam.objects.filter(user=kwargs.get('pk'))
        user_games = list()
        now = timezone.now()
        for _ in user_in_teams:
            games = Game.objects.filter(timespan__lt=now).order_by('-timespan')
            for game in games:
                user_games.append(game)
        data = GameSerializer(user_games, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UserFutureGamesListView(ListAPIView):
    """Class that implements user future quests list view API endpoint"""

    serializer_class = GameSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def get(request, *args, **kwargs):
        user_in_teams = UserInTeam.objects.filter(user=kwargs.get('pk'))
        user_games = list()
        now = timezone.now()
        for _ in user_in_teams:
            games = Game.objects.filter(timespan__gte=now).order_by('timespan')
            for game in games:
                user_games.append(game)
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
                        'message': 'Not enough credits on Prostor SMS account!',
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
                    }, status=status.HTTP_200_OK)
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
