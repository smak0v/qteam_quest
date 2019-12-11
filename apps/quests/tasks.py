from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone

from apps.quests.models import Game


@periodic_task(run_every=(crontab(minute='*/1')),
               name='close_registration_one_hour_before_the_game',
               ignore_result=True)
def close_registration_one_hour_before_the_game():
    games = Game.objects.filter(timespan__year=timezone.now().year,
                                timespan__month=timezone.now().month,
                                timespan__day=timezone.now().day)
    for game in games:
        game.check_registration_availability()
