from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.timeline.api_views import TimelineAPIView
from apps.timeline.views import create_timeline_block_view, timeline_blocks_list_view, edit_timeline_block_view, \
    delete_timeline_block_view

timeline_api_urls = (
    [
        path('<int:pk>/', TimelineAPIView.as_view(), name='timeline'),
    ], 'api:timeline')

timeline_urls = (
    [
        path('', login_required(timeline_blocks_list_view), name='list'),
        path('create_block/', login_required(create_timeline_block_view), name='create_block'),
        path('edit_block/<int:pk>/', login_required(edit_timeline_block_view), name='edit_block'),
        path('delete_block/<int:pk>/', login_required(delete_timeline_block_view), name='delete_block'),
    ], 'timeline')
