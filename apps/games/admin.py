from django.contrib import admin

from apps.games.models import Game, GameComment, GamePlayerEvaluation


class GameAdmin(admin.ModelAdmin):
    """Class that represents admin part of game"""

    ordering = [
        'title',
        'genre',
        'timespan',
        'duration',
        'quest',
        'payment_method',
        'price',
        'currency',
        'level',
        'min_players_count',
        'max_players_count',
        'players_count',
        'registration_available',
        'cancel',
    ]
    list_display = [
        'title',
        'genre',
        'timespan',
        'duration',
        'quest',
        'payment_method',
        'price',
        'currency',
        'level',
        'min_players_count',
        'max_players_count',
        'players_count',
        'registration_available',
        'cancel',
    ]
    list_filter = [
        'genre',
        'timespan',
        'duration',
        'quest',
        'payment_method',
        'currency',
        'level',
        'refund_money_if_game_is_cancelled',
        'registration_available',
        'cancel',
    ]
    search_fields = [
        'title',
        'description',
        'genre',
        'timespan',
        'duration',
        'quest',
        'payment_method',
        'price',
        'currency',
        'level',
        'refundable_days',
        'min_players_count',
        'max_players_count',
        'players_count',
        'registration_available',
        'cancel',
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
