import logging

from celery.schedules import crontab
from celery.task import periodic_task

from apps.games.models import Game

logger = logging.getLogger(__name__)


@periodic_task(run_every=(crontab(minute='*/1')),
               name='close_registration_one_hour_before_the_game',
               ignore_result=True)
def close_registration_one_hour_before_the_game():
    games = Game.objects.all()
    logger.debug("close_registration_one_hour_before_the_game")
    for game in games:
        game.check_registration_availability()
