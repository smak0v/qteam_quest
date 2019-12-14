from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.venues.api_views import VenueListCreateView, VenueRetrieveUpdateDestroyView, VenueSubscribersListView, \
    VenueGamesListView, VenueSubscribeCreateView, VenueSubscribeDestroyView, VenueCommentListCreateView
from apps.venues.views import VenuesListView, delete_venue_view, edit_venue_view, create_venue_view, \
    venue_details_view, create_venue_metro_station_view, edit_venue_metro_station_view, delete_venue_metro_station_view

venues_urls = (
    [
        path('', login_required(VenuesListView.as_view()), name='list'),
        path('details/<int:pk>/', login_required(venue_details_view), name='details'),
        path('create/', login_required(create_venue_view), name='create'),
        path('edit/<int:pk>/', login_required(edit_venue_view), name='edit'),
        path('delete/<int:pk>/', login_required(delete_venue_view), name='delete'),
        path('<int:venue_pk>/metro_stations/create/', login_required(create_venue_metro_station_view),
             name='create_metro_station'),
        path('<int:venue_pk>/metro_stations/<int:station_pk>/edit/', login_required(edit_venue_metro_station_view),
             name='edit_metro_station'),
        path('<int:venue_pk>/metro_stations/<int:station_pk>/delete/', login_required(delete_venue_metro_station_view),
             name='delete_metro_station'),
    ], 'venues')

venues_api_urls = (
    [
        path('', VenueListCreateView.as_view(), name='venues_list'),
        path('<int:pk>/', VenueRetrieveUpdateDestroyView.as_view(), name='venue_detail'),
        path('<int:pk>/games/', VenueGamesListView.as_view(), name='venue_games'),
        path('<int:pk>/subscribers/', VenueSubscribersListView.as_view(), name='venue_subscribers'),
        path('<int:pk>/subscribe/', VenueSubscribeCreateView.as_view(), name='venue_subscribe'),
        path('<int:pk>/unsubscribe/', VenueSubscribeDestroyView.as_view(), name='venue_unsubscribe'),
        path('<int:pk>/comments/', VenueCommentListCreateView.as_view(), name='venue_comments'),
    ], 'api:venues')
