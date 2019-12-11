from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.quests.api_views import GameRetrieveUpdateDestroyView, GameCommentListCreateView, \
    GameTeamsListView, GamePlayersListCreateView, GameReservedPlacesListCreateView, GamePlayersRetrieveDestroyView, \
    GameReservedPlacesRetrieveDestroyView, GameListCreateView, GamePlacesStatusView, EvaluatePlayerView
from apps.quests.views import GamesListView, create_game_view, edit_game_view, delete_game_view, details_game_view, \
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
    ], 'quests')

games_api_urls = (
    [
        path('', GameListCreateView.as_view(), name='games_list'),
        path('<int:pk>/', GameRetrieveUpdateDestroyView.as_view(), name='game_detail'),
        path('<int:pk>/comments/', GameCommentListCreateView.as_view(), name='game_comments'),
        path('<int:pk>/teams/', GameTeamsListView.as_view(), name='game_teams'),
        path('<int:pk>/players/', GamePlayersListCreateView.as_view(), name='game_players'),
        path('<int:pk>/players/<int:player_pk>/', GamePlayersRetrieveDestroyView.as_view(),
             name='game_players_detail'),
        path('<int:pk>/reserved_places/', GameReservedPlacesListCreateView.as_view(), name='game_reserved_places'),
        path('<int:pk>/reserved_places/<int:reserve_user_pk>/', GameReservedPlacesRetrieveDestroyView.as_view(),
             name='game_reserved_places_detail'),
        path('<int:pk>/places_status/', GamePlacesStatusView.as_view(), name='game_places_status'),
        path('<int:pk>/evaluate_player/', EvaluatePlayerView.as_view(), name='game_player_evaluation'),
    ], 'api:quests')
