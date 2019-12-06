import os
import random

from django.core.management.base import BaseCommand

from apps.venues.models import Venue, MetroStation


class Command(BaseCommand):
    help = 'Add metro stations for venues'

    def handle(self, *args, **options):
        stations = self.get_metro_station_names()
        MetroStation.objects.all().delete()
        for venue in Venue.objects.all():
            for i in range(random.randint(3, 6)):
                MetroStation.objects.create(
                    name=random.choice(stations),
                    color=("#%06x" % random.randint(0, 0xFFFFFF)),
                    venue=venue)

    @staticmethod
    def get_metro_station_names():
        filename = os.path.join("scripts", "text", "Moscow_metro_stations.txt")
        stations = []
        with open(filename, 'r') as f:
            for line in f:
                text = line.strip()
                if text != '':
                    stations.append(text)
        return stations
