from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.quests.api_views import QuestListCreateView, QuestRetrieveUpdateDestroyView, QuestSubscribersListView, \
    QuestGamesListView, QuestSubscribeCreateView, QuestSubscribeDestroyView, QuestCommentListCreateView
from apps.quests.views import QuestListView, delete_quest_view, edit_quest_view, create_quest_view, \
    quest_details_view, create_quest_metro_station_view, edit_quest_metro_station_view, delete_quest_metro_station_view

quests_urls = (
    [
        path('', login_required(QuestListView.as_view()), name='list'),
        path('details/<int:pk>/', login_required(quest_details_view), name='details'),
        path('create/', login_required(create_quest_view), name='create'),
        path('edit/<int:pk>/', login_required(edit_quest_view), name='edit'),
        path('delete/<int:pk>/', login_required(delete_quest_view), name='delete'),
        path('<int:quest_pk>/metro_stations/create/', login_required(create_quest_metro_station_view),
             name='create_metro_station'),
        path('<int:quest_pk>/metro_stations/<int:station_pk>/edit/', login_required(edit_quest_metro_station_view),
             name='edit_metro_station'),
        path('<int:quest_pk>/metro_stations/<int:station_pk>/delete/', login_required(delete_quest_metro_station_view),
             name='delete_metro_station'),
    ], 'quests')

quests_api_urls = (
    [
        path('', QuestListCreateView.as_view(), name='quests_list'),
        path('<int:pk>/', QuestRetrieveUpdateDestroyView.as_view(), name='quest_detail'),
        path('<int:pk>/games/', QuestGamesListView.as_view(), name='quest_games'),
        path('<int:pk>/subscribers/', QuestSubscribersListView.as_view(), name='quest_subscribers'),
        path('<int:pk>/subscribe/', QuestSubscribeCreateView.as_view(), name='quest_subscribe'),
        path('<int:pk>/unsubscribe/', QuestSubscribeDestroyView.as_view(), name='quest_unsubscribe'),
        path('<int:pk>/comments/', QuestCommentListCreateView.as_view(), name='quest_comments'),
    ], 'api:quests')
