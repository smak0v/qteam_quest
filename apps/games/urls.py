from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.games.api_views import GameRetrieveUpdateDestroyView, GameCommentListCreateView, \
    GameTeamListView, GamePlayersListView, GamePlayersRetrieveView, GameListCreateView, GamePlacesStatusView, \
    EvaluatePlayerView, GameReserveTemporaryPlaceCreateView, GameReserveTemporaryPlaceDestroyView, \
    GameReservedPlacesInfoView, GamePaymentTokenView, GameUnregisterBookedPlacesAPIView
from apps.games.views import GamesListView, create_game_view, edit_game_view, delete_game_view, details_game_view, \
    cancel_game_view, renew_game_view

games_urls = (
    [
        path('', login_required(GamesListView.as_view()), name='list'),
        path('create/', login_required(create_game_view), name='create'),
        path('edit/<int:pk>/', login_required(edit_game_view), name='edit'),
        path('delete/<int:pk>/', login_required(delete_game_view), name='delete'),
        path('details/<int:pk>/', login_required(details_game_view), name='details'),
        path('cancel/<int:pk>/', login_required(cancel_game_view), name='cancel'),
        path('renew/<int:pk>/', login_required(renew_game_view), name='renew'),
    ], 'games')

games_api_urls = (
    [
        path('', GameListCreateView.as_view(), name='games_list'),
        path('<int:pk>/', GameRetrieveUpdateDestroyView.as_view(), name='game_detail'),
        path('<int:pk>/comments/', GameCommentListCreateView.as_view(), name='game_comments'),
        path('<int:pk>/team/', GameTeamListView.as_view(), name='game_team'),
        path('<int:pk>/places_status/', GamePlacesStatusView.as_view(), name='game_places_status'),
        path('<int:pk>/reserve_place/', GameReserveTemporaryPlaceCreateView.as_view(),
             name='game_reserve_temporary_place'),
        path('<int:pk>/unreserve_place/', GameReserveTemporaryPlaceDestroyView.as_view(),
             name='game_destroy_temporary_place'),
        path('<int:pk>/reserved_places_info/', GameReservedPlacesInfoView.as_view(), name='game_reserved_places_info'),
        path('<int:pk>/payment_token/', GamePaymentTokenView.as_view(), name='game_payment_token'),
        path('<int:pk>/unregister_booked_places/', GameUnregisterBookedPlacesAPIView.as_view(),
             name='game_unregister_booked_places'),
        path('<int:pk>/players/', GamePlayersListView.as_view(), name='game_players'),
        path('<int:pk>/players/<int:player_pk>/', GamePlayersRetrieveView.as_view(), name='game_players_detail'),
        path('<int:pk>/evaluate_player/', EvaluatePlayerView.as_view(), name='game_player_evaluation'),
    ], 'api:games')
