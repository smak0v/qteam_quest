from django.contrib import admin

from apps.teams.models import Team, UserInTeam, ReservedPlaceInTeam


class TeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of a team"""

    list_display = [
        'game',
        'name',
    ]
    ordering = [
        'game',
        'name',
    ]
    list_per_page = 50


class UserInTeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of the user in a team"""

    list_display = [
        'team',
        'user',
    ]
    ordering = [
        'team',
        'user',
    ]
    list_per_page = 50


class ReservedPlaceInTeamAdmin(admin.ModelAdmin):
    """Class that represents admin part of the reserved place in a team"""

    list_display = [
        'team',
        'user',
        'title',
    ]
    ordering = [
        'team',
        'user',
        'title',
    ]
    list_per_page = 50


admin.site.register(Team, TeamAdmin)
admin.site.register(UserInTeam, UserInTeamAdmin)
admin.site.register(ReservedPlaceInTeam, ReservedPlaceInTeamAdmin)
