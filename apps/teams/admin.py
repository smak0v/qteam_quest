from django.contrib import admin

from apps.teams.models import Team, UserInTeam, TemporaryReserve


class TeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of a team"""

    list_display = [
        'pk',
        'game',
    ]
    ordering = [
        'pk',
        'game',
    ]
    list_per_page = 50


class UserInTeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of the user in a team"""

    list_display = [
        'pk',
        'game',
        'team',
        'user',
        'title',
        'payment',
    ]
    ordering = [
        'pk',
        'game',
        'team',
        'user',
        'title',
        'payment',
    ]
    search_fields = [
        'title',
    ]
    list_per_page = 50


class TemporaryReserveAdmin(admin.ModelAdmin):
    """"Class that represents admin part of the temporary reserve (5 minutes) of one place in team for the game"""

    list_display = [
        'pk',
        'game',
        'user',
    ]
    ordering = [
        'pk',
        'game',
        'user',
    ]
    list_per_page = 50


admin.site.register(Team, TeamAdmin)
admin.site.register(UserInTeam, UserInTeamAdmin)
admin.site.register(TemporaryReserve, TemporaryReserveAdmin)
