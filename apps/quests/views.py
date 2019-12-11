from django.shortcuts import render, redirect
from django.views import View

from apps.quests.forms import GameForm
from apps.quests.models import Game
from apps.teams.models import Team, UserInTeam, ReservedPlaceInTeam


class GamesListView(View):
    """Class that implements quests list view"""

    template_name = 'quests/list.html'

    def get(self, request):
        games = Game.objects.filter(cancel=False).order_by('timespan')
        canceled_games = Game.objects.filter(cancel=True).order_by('timespan')
        context = {
            'title': 'Игры',
            'quests': games,
            'canceled_games': canceled_games,
        }
        return render(request=request, template_name=self.template_name, context=context)


def details_game_view(request, pk):
    """Function that implements game details view"""

    game = Game.objects.get(pk=pk)
    team_1 = Team.objects.filter(game=game).first()
    team_2 = Team.objects.filter(game=game).last()
    team_1_players = UserInTeam.objects.filter(game=game, team=team_1)
    team_2_players = UserInTeam.objects.filter(game=game, team=team_2)
    team_1_reserved_places = ReservedPlaceInTeam.objects.filter(game=game, team=team_1)
    team_2_reserved_places = ReservedPlaceInTeam.objects.filter(game=game, team=team_2)
    context = {
        'title': 'Информация об игре',
        'game': game,
        'team_1': team_1,
        'team_2': team_2,
        'team_1_players': team_1_players,
        'team_2_players': team_2_players,
        'team_1_reserved_places': team_1_reserved_places,
        'team_2_reserved_places': team_2_reserved_places,
    }
    return render(request=request, template_name='quests/details.html', context=context)


def create_game_view(request, venue=None):
    """Function that implements game create view for a venue"""

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            team_1 = Team.objects.create(
                game=game,
                name='Черные майки',
                players_count_per_team=game.a_side_players_count,
            )
            team_2 = Team.objects.create(
                game=game,
                name='Белые майки',
                players_count_per_team=game.a_side_players_count,
            )
            return redirect(to='quests:list')
        else:
            context = {
                'title': 'Создание игры',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='quests/create.html', context=context)
    else:
        form = GameForm()
        context = {
            'form': form,
            'title': 'Создание игры',
        }
        return render(request=request, template_name='quests/create.html', context=context)


def edit_game_view(request, pk):
    """Function that implements game edit view"""

    game = Game.objects.get(pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect(to='quests:list')
        else:
            context = {
                'title': 'Редактирование игры',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='quests/edit.html', context=context)
    else:
        form = GameForm(instance=game)
        context = {
            'form': form,
            'title': 'Редактирование игры',
        }
        return render(request=request, template_name='quests/edit.html', context=context)


def delete_game_view(request, pk):
    """Function that implements game delete view"""

    game = Game.objects.get(pk=pk)
    game.delete()
    return redirect(to='quests:list')


def cancel_game_view(request, pk):
    """Function that implements game cancel view"""

    game = Game.objects.get(pk=pk)
    game.cancel = True
    game.registration_available = False
    game.save()
    return redirect(to='quests:list')


def renew_game_view(request, pk):
    """Function that implements game renew view"""

    game = Game.objects.get(pk=pk)
    game.cancel = False
    game.registration_available = True
    game.save()
    return redirect(to='quests:list')
