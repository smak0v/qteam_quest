from django.contrib import admin

from apps.venues.models import Venue, VenueComment, VenueSubscription, MetroStation


class VenueAdmin(admin.ModelAdmin):
    """Class that represents admin part of the venue"""

    ordering = [
        'name',
        'location',
        'rating',
    ]
    list_display = [
        'name',
        'location',
        'rating',
        'x_coordinate',
        'y_coordinate',
    ]
    search_fields = [
        'name',
        'location',
    ]
    list_per_page = 50


class VenueCommentAdmin(admin.ModelAdmin):
    """Class that represents admin part of the venue comment"""

    ordering = [
        'venue',
        'user',
        'scores',
    ]
    list_display = [
        'venue',
        'user',
        'scores',
    ]
    search_fields = [
        'venue',
        'user',
        'text',
        'scores',
    ]
    list_filter = [
        'timestamp',
    ]
    list_per_page = 50


class VenueSubscriptionAdmin(admin.ModelAdmin):
    """Class that represents admin part of the venue subscriptions"""

    list_display = [
        'user',
        'venue',
    ]
    ordering = [
        'user',
        'venue',
    ]
    search_fields = [
        'user',
        'venue',
    ]
    list_per_page = 50


class MetroStationAdmin(admin.ModelAdmin):
    """Class that represents admin part of the metro station"""

    list_display = [
        'name',
        'color',
        'venue',
    ]
    ordering = [
        'name',
        'color',
        'venue',
    ]
    search_fields = [
        'name',
        'color',
        'venue',
    ]
    list_per_page = 50


admin.site.register(Venue, VenueAdmin)
admin.site.register(VenueComment, VenueCommentAdmin)
admin.site.register(VenueSubscription, VenueSubscriptionAdmin)
admin.site.register(MetroStation, MetroStationAdmin)
