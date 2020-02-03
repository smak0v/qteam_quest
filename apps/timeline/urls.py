from django.urls import path

from apps.timeline.api_views import TimelineAPIView

timeline_api_urls = (
    [
        path('<int:pk>/', TimelineAPIView.as_view(), name='timeline'),
    ], 'api:timeline')
