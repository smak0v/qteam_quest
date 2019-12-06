from django.contrib import admin

from apps.teams.models import Team, UserInTeam, ReservedPlaceInTeam


class TeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of a team"""

    list_display = [
        'game',
        'name',
        'players_count_per_team',
    ]
    ordering = [
        'game',
        'name',
        'players_count_per_team',
    ]
    list_filter = [
        'players_count_per_team',
    ]
    list_per_page = 50


class UserInTeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of the user in a team"""

    list_display = [
        'team',
        'user',
        'user_position',
    ]
    ordering = [
        'team',
        'user',
        'user_position',
    ]
    list_filter = [
        'user_position',
    ]
    list_per_page = 50


class ReservedPlaceInTeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of the reserved place in a team"""

    list_display = [
        'team',
        'user',
        'title',
        'reserved_position',
    ]
    ordering = [
        'team',
        'user',
        'title',
        'reserved_position',
    ]
    list_filter = [
        'reserved_position',
    ]
    list_per_page = 50


admin.site.register(Team, TeamAdmin)
admin.site.register(UserInTeam, UserInTeamAdmin)
admin.site.register(ReservedPlaceInTeam, ReservedPlaceInTeamAdmin)
