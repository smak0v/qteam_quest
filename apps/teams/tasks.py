from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone

from apps.games.models import Game
from apps.teams.models import TemporaryReserve


@periodic_task(run_every=(crontab(minute='*/1')),
               name='remove_reserved_temporary_place_after_five_minutes',
               ignore_result=True)
def remove_reserved_temporary_place_after_five_minutes():
    places = TemporaryReserve.objects.filter(timespan__lte=timezone.now() - timezone.timedelta(minutes=10))
    for place in places:
        game = Game.objects.get(pk=place.game.pk)
        place.delete()
        game.players_count -= 1
        game.save()
