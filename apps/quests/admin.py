from django.contrib import admin

from apps.quests.models import Quest, QuestComment, QuestSubscription, MetroStation


class QuestAdmin(admin.ModelAdmin):
    """Class that represents admin part of the quests"""

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
        'description',
        'location',
    ]
    list_per_page = 50


class QuestCommentAdmin(admin.ModelAdmin):
    """Class that represents admin part of the quests comment"""

    ordering = [
        'quest',
        'user',
        'scores',
    ]
    list_display = [
        'quest',
        'user',
        'scores',
    ]
    search_fields = [
        'quest',
        'user',
        'text',
        'scores',
    ]
    list_filter = [
        'timestamp',
    ]
    list_per_page = 50


class QuestSubscriptionAdmin(admin.ModelAdmin):
    """Class that represents admin part of the quests subscriptions"""

    list_display = [
        'user',
        'quest',
    ]
    ordering = [
        'user',
        'quest',
    ]
    search_fields = [
        'user',
        'quest',
    ]
    list_per_page = 50


class MetroStationAdmin(admin.ModelAdmin):
    """Class that represents admin part of the metro station"""

    list_display = [
        'name',
        'color',
        'quest',
    ]
    ordering = [
        'name',
        'color',
        'quest',
    ]
    search_fields = [
        'name',
        'color',
        'quest',
    ]
    list_per_page = 50


admin.site.register(Quest, QuestAdmin)
admin.site.register(QuestComment, QuestCommentAdmin)
admin.site.register(QuestSubscription, QuestSubscriptionAdmin)
admin.site.register(MetroStation, MetroStationAdmin)
