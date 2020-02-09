from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from yandex_checkout import Payment, Configuration

from apps.games.forms import GameForm
from apps.games.models import Game, GamePayment
from apps.payment.utils import create_refund
from apps.teams.models import Team, UserInTeam
from apps.timeline.utils import create_timeline_block


class GamesListView(View):
    """Class that implements games list view"""

    @staticmethod
    def get(request):
        games = Game.objects.filter(cancel=False).order_by('timespan')
        canceled_games = Game.objects.filter(cancel=True).order_by('timespan')
        context = {
            'title': 'Игры',
            'games': games,
            'canceled_games': canceled_games,
        }
        return render(request=request, template_name='games/list.html', context=context)


def details_game_view(request, pk):
    """Function that implements game details view"""

    game = Game.objects.get(pk=pk)
    team = Team.objects.filter(game=game).first()
    team_players = UserInTeam.objects.filter(game=game, team=team)
    context = {
        'title': 'Информация об игре',
        'game': game,
        'team': team,
        'team_players': team_players,
    }
    return render(request=request, template_name='games/details.html', context=context)


def create_game_view(request, venue=None):
    """Function that implements game create view for a venue"""

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            team = Team.objects.create(
                game=game,
            )
            return redirect(to='games:list')
        else:
            context = {
                'title': 'Создание игры',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='games/create.html', context=context)
    else:
        form = GameForm()
        context = {
            'form': form,
            'title': 'Создание игры',
        }
        return render(request=request, template_name='games/create.html', context=context)


def edit_game_view(request, pk):
    """Function that implements game edit view"""

    game = Game.objects.get(pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect(to='games:list')
        else:
            context = {
                'title': 'Редактирование игры',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='games/edit.html', context=context)
    else:
        form = GameForm(instance=game)
        context = {
            'form': form,
            'title': 'Редактирование игры',
        }
        return render(request=request, template_name='games/edit.html', context=context)


def delete_game_view(request, pk):
    """Function that implements game delete view"""

    game = Game.objects.get(pk=pk)
    game.delete()
    return redirect(to='games:list')


def cancel_game_view(request, pk):
    """Function that implements game cancel view"""

    Configuration.account_id = settings.YANDEX_ACCOUNT_ID
    Configuration.secret_key = settings.YANDEX_SECRET_KEY
    game = Game.objects.get(pk=pk)
    game.cancel = True
    game.registration_available = False
    game.save()
    users_in_game = UserInTeam.objects.filter(game=game)
    for user_in_game in users_in_game:
        create_timeline_block('GAME_MESSAGE', settings.GAME_CANCELED, user_in_game.user, 'APP', game)
        user_in_game.delete()
    game_payments = GamePayment.objects.filter(game=game, status='SUCCEEDED')
    for game_payment in game_payments:
        payment = Payment.find_one(game_payment.identifier)
        if payment.status == 'succeeded':
            create_refund(game_payment, game_payment.user, game_payment.game)
    return redirect(to='games:list')


def renew_game_view(request, pk):
    """Function that implements game renew view"""

    game = Game.objects.get(pk=pk)
    game.cancel = False
    game.registration_available = True
    game.save()
    return redirect(to='games:list')
