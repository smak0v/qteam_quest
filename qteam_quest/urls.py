"""
qteam_quest URL Configuration
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.coupons.urls import coupons_urls, coupons_api_urls
from apps.dashboard.urls import dashboard_urls
from apps.games.urls import games_urls, games_api_urls
from apps.payment.urls import payment_api_urls
from apps.quests.urls import quests_urls, quests_api_urls
from apps.teams.urls import teams_urls, teams_api_urls
from apps.timeline.urls import timeline_api_urls, timeline_urls
from qteam_quest import settings
from users.urls import users_urls, users_api_urls

urlpatterns = [
    # Admin urls
    path('admin/', admin.site.urls),

    # Apps urls
    path('', include(dashboard_urls)),
    path('games/', include(games_urls)),
    path('quests/', include(quests_urls)),
    path('accounts/', include(users_urls)),
    path('teams/', include(teams_urls)),
    path('coupons/', include(coupons_urls)),
    path('timeline/', include(timeline_urls)),

    # API urls
    path('api/games/', include(games_api_urls)),
    path('api/quests/', include(quests_api_urls)),
    path('api/teams/', include(teams_api_urls)),
    path('api/users/', include(users_api_urls)),
    path('api/coupons/', include(coupons_api_urls)),
    path('api/payment/', include(payment_api_urls)),
    path('api/timeline/', include(timeline_api_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
