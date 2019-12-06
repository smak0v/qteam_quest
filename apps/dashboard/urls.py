from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.dashboard.views import DashboardView

dashboard_urls = (
    [
        path('', login_required(DashboardView.as_view()), name='dashboard'),
    ], 'dashboard')
