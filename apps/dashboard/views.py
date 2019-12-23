from django.shortcuts import render
from django.utils import timezone
from django.views import View

from apps.games.models import Game


class DashboardView(View):
    """Class that represents dashboard view"""

    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        # Statistic
        games = Game.objects.all()

        opened_for_registration_games = Game.objects.filter(registration_available=True)

        canceled_games = Game.objects.filter(cancel=True)

        # Today statistic
        today_games = Game.objects.filter(timespan__day=timezone.now().day,
                                          timespan__month=timezone.now().month,
                                          timespan__year=timezone.now().year)

        today_held_games = list()
        for today_game in today_games:
            if timezone.now() >= today_game.timespan + timezone.timedelta(minutes=today_game.duration):
                if not today_game.registration_available and not today_game.cancel:
                    today_held_games.append(today_game)

        today_failed_games = list()
        for today_game in today_games:
            if timezone.now() >= today_game.timespan + timezone.timedelta(minutes=today_game.duration):
                if not today_game.registration_available and today_game.cancel:
                    today_failed_games.append(today_games)

        today_canceled_games = list()
        for today_game in today_games:
            if today_game.cancel:
                today_canceled_games.append(today_games)

        context = {
            'title': 'Дашборд',
            'games': games,
            'opened_for_registration_games': opened_for_registration_games,
            'canceled_games': canceled_games,
            'today_held_games': today_held_games,
            'today_failed_games': today_failed_games,
            'today_canceled_games': today_canceled_games,
        }
        return render(request=request, template_name=self.template_name, context=context)
