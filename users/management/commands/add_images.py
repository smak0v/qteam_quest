import os

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.games.models import Game
from apps.venues.models import Venue
from users.models import User


class Command(BaseCommand):
    help = 'Add images for objects'

    def handle(self, *args, **options):
        users = User.objects.filter(username__startswith='test_user_')
        self.set_images(users, "avatars", "{}.jpg", "profile_image")

        games = Game.objects.all()
        self.set_images(games, "game_photos", "fc_{}.jpg", "photo")
        self.set_images(games, "game_covers", "game_{}.jpg", "cover_image")

        venues = Venue.objects.all()
        self.set_images(venues, "venue_photos", "flag_{}.png", "photo")
        self.set_images(venues, "venue_covers", "venue_{}.jpg", "cover_image")

    @staticmethod
    def set_images(objects, folder, file_template, field_name):
        images_count = len(os.listdir(os.path.join("scripts", "images", folder)))
        i = 1
        for obj in objects:
            file_name = file_template.format(i)
            with open(os.path.join("scripts", "images", folder, file_name), 'rb') as f:
                field = getattr(obj, field_name)
                field.save(file_name, File(f))
            i += 1
            if i > images_count:
                i = 1
