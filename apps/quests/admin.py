from django.contrib import admin

from apps.quests.models import Game, GameComment, GamePlayerEvaluation


class GameAdmin(admin.ModelAdmin):
    """Class that represents admin part of game"""

    ordering = [
        'title',
        'timespan',
        'duration',
        'venue',
        'game_status',
        'price',
        'cancel',
        'registration_available',
    ]
    list_display = [
        'title',
        'timespan',
        'duration',
        'venue',
        'game_status',
        'price',
        'cancel',
        'registration_available',
    ]
    list_filter = [
        'timespan',
        'currency',
        'game_status',
        'a_side_players_count',
        'cancel',
        'registration_available',
    ]
    search_fields = [
        'title',
        'timespan',
        'duration',
        'venue',
        'currency',
        'game_status',
    ]
    list_per_page = 50


class GameCommentAdmin(admin.ModelAdmin):
    """Class that represents admin part of the game comment"""

    list_display = [
        'user',
        'game',
    ]
    ordering = [
        'user',
        'game',
    ]
    search_fields = [
        'user',
        'game',
        'text',
    ]
    list_filter = [
        'timestamp',
    ]
    list_per_page = 50


class GamePlayerEvaluationAdmin(admin.ModelAdmin):
    """Class that represents admin part of the game player evaluation"""

    list_display = [
        'game',
        'appraiser',
        'ranked_user',
        'game_level',
        'enjoyed_playing',
    ]
    ordering = [
        'game',
        'appraiser',
        'ranked_user',
        'game_level',
        'enjoyed_playing'
    ]
    search_fields = [
        'game',
        'appraiser',
        'ranked_user',
        'game_level',
        'enjoyed_playing'
    ]
    list_filter = [
        'game_level',
        'enjoyed_playing'
    ]
    list_per_page = 50


admin.site.register(Game, GameAdmin)
admin.site.register(GameComment, GameCommentAdmin)
admin.site.register(GamePlayerEvaluation, GamePlayerEvaluationAdmin)
