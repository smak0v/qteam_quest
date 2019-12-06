from django.urls import path

from users.api_views import UserRegisterView, UserListView, UserVenueSubscriptionsListView, UserSubscribersListView, \
    UserSubscriptionsListView, UserSubscribeView, UserUnsubscribeView, UserGamesListView, UserPastGamesListView, \
    UserFutureGamesListView, UserRetrieveUpdateDeleteView, UserChangePasswordView, ChangePhoneView, \
    ChangePhoneConfirmView, UserProfileView
from users.views import login_view, signup_view, logout_view

users_urls = (
    [
        path('login/', login_view, name='login'),
        path('signup/', signup_view, name='signup'),
        path('logout/', logout_view, name='logout'),
    ], 'accounts')

users_api_urls = (
    [
        path('', UserListView.as_view(), name='list'),
        path('my_profile/', UserProfileView.as_view(), name='user_profile'),
        path('register/', UserRegisterView.as_view(), name='register'),
        path('<int:pk>/', UserRetrieveUpdateDeleteView.as_view(), name='user_detail'),
        path('<int:pk>/change_password/', UserChangePasswordView.as_view(), name='user_change_password'),
        path('<int:pk>/change_phone/', ChangePhoneView.as_view(), name='user_change_phone'),
        path('<int:pk>/change_phone_confirm/', ChangePhoneConfirmView.as_view(), name='user_change_phone_confirm'),
        path('<int:pk>/venue_subscriptions/', UserVenueSubscriptionsListView.as_view(), name='venue_subscriptions'),
        path('<int:pk>/subscribers/', UserSubscribersListView.as_view(), name='user_subscribers'),
        path('<int:pk>/subscriptions/', UserSubscriptionsListView.as_view(), name='user_subscriptions'),
        path('<int:pk>/subscribe/', UserSubscribeView.as_view(), name='user_subscribe'),
        path('<int:pk>/unsubscribe/', UserUnsubscribeView.as_view(), name='user_unsubscribe'),
        path('<int:pk>/games/', UserGamesListView.as_view(), name='user_games'),
        path('<int:pk>/past_games/', UserPastGamesListView.as_view(), name='user_past_games'),
        path('<int:pk>/future_games/', UserFutureGamesListView.as_view(), name='user_future_games'),
    ], 'api:users')
