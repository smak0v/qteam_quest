from django.contrib import admin

from apps.games.models import Game, GameComment, GamePlayerEvaluation, GamePayment


class GameAdmin(admin.ModelAdmin):
    """Class that represents admin part of game"""

    ordering = [
        'pk',
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
        'pk',
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
        'pk',
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
        'pk',
        'user',
        'game',
    ]
    ordering = [
        'pk',
        'user',
        'game',
    ]
    search_fields = [
        'pk',
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
        'pk',
        'game',
        'appraiser',
        'ranked_user',
        'game_level',
        'enjoyed_playing',
    ]
    ordering = [
        'pk',
        'game',
        'appraiser',
        'ranked_user',
        'game_level',
        'enjoyed_playing'
    ]
    search_fields = [
        'pk',
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


class GamePaymentAdmin(admin.ModelAdmin):
    """Class that implements admin part of the user payment for the game"""

    list_display = [
        'identifier',
        'user',
        'game',
        'coupon',
        'summa',
        'discount',
        'discount_units',
        'summa_with_discount',
        'currency',
        'places_count',
    ]
    ordering = [
        'identifier',
        'user',
        'game',
        'coupon',
        'summa',
        'discount',
        'discount_units',
        'summa_with_discount',
        'currency',
        'places_count',
    ]
    search_fields = [
        'identifier',
        'user',
        'game',
        'coupon',
        'summa',
        'discount',
        'discount_units',
        'summa_with_discount',
        'currency',
        'places_count',
    ]
    list_filter = [
        'discount_units',
        'currency',
    ]
    list_per_page = 50


admin.site.register(Game, GameAdmin)
admin.site.register(GameComment, GameCommentAdmin)
admin.site.register(GamePlayerEvaluation, GamePlayerEvaluationAdmin)
admin.site.register(GamePayment, GamePaymentAdmin)
