from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.games.api_views import GameRetrieveUpdateDestroyView, GameCommentListCreateView, \
    GameTeamListView, GamePlayersListCreateView, GamePlayersRetrieveDestroyView, \
    GameListCreateView, GamePlacesStatusView, EvaluatePlayerView, GameReserveTemporaryPlaceCreateView, \
    GameReserveTemporaryPlaceDestroyView, GameBookPlacesView
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

        # TODO and check
        path('<int:pk>/book_places/', GameBookPlacesView.as_view(), name='book_places'),
        path('<int:pk>/players/', GamePlayersListCreateView.as_view(), name='game_players'),
        path('<int:pk>/players/<int:player_pk>/', GamePlayersRetrieveDestroyView.as_view(),
             name='game_players_detail'),
        path('<int:pk>/evaluate_player/', EvaluatePlayerView.as_view(), name='game_player_evaluation'),
    ], 'api:games')
