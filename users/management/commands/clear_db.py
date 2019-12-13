from django.core.management.base import BaseCommand

from apps.coupons.models import Coupon
from apps.venues.models import Venue
from users.models import User


class Command(BaseCommand):
    help = 'Clear database'

    def handle(self, *args, **options):
        self.delete_venues_and_related_objects()
        self.delete_users_and_related_objects()
        self.delete_coupons()

    @staticmethod
    def delete_users_and_related_objects():
        users = User.objects.filter(admin=False)
        if len(users) > 0:
            print('Removing users and all related objects:')
            for user in users:
                user.delete()
                print('.', end='', flush=True)
            print('\nRemoving users and all related objects: DONE.')
        else:
            print('No users in DB.')

    @staticmethod
    def delete_venues_and_related_objects():
        venues = Venue.objects.all()
        if len(venues) > 0:
            print('Removing venues and all related objects:')
            for venue in venues:
                venue.delete()
                print('.', end='', flush=True)
            print('\nRemoving venues and all related objects: DONE.')
        else:
            print('No venues in DB.')

    @staticmethod
    def delete_coupons():
        coupons = Coupon.objects.all()
        if len(coupons) > 0:
            print('Removing coupons:')
            for coupon in coupons:
                coupon.delete()
                print('.', end='', flush=True)
            print('\nRemoving coupons: DONE.')
        else:
            print('No coupons in DB.')
