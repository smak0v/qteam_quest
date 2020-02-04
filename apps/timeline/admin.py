from django.contrib import admin

from apps.timeline.models import TimelineBlock


class TimelineBlockAdmin(admin.ModelAdmin):
    """"Class that represents admin part of a timeline block element"""

    list_display = [
        'pk',
        'type',
        'timespan',
        'message',
        'user',
        'game',
    ]
    ordering = [
        'pk',
        'type',
        'timespan',
        'message',
        'user',
        'game',
    ]
    search_fields = [
        'type',
        'timespan',
        'message',
        'user',
        'game',
    ]
    list_per_page = 50


admin.site.register(TimelineBlock, TimelineBlockAdmin)
