import calendar
import os
import random
from datetime import datetime
from time import gmtime

import pytz
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.coupons.models import Coupon
from apps.games.models import Game, GameComment
from apps.quests.models import Quest, MetroStation, QuestComment, QuestSubscription, QuestImage
from apps.teams.models import Team, UserInTeam
from users.models import User, UserSubscription


class Command(BaseCommand):
    help = 'Fill database'

    users_count = random.randint(5, 20)
    quests_count = random.randint(5, 20)
    coupons_count = random.randint(5, 20)
    games_count_per_day = random.randint(5, 10)
    comments_count = random.randint(5, 50)
    subscriptions_count = random.randint(5, 20)
    game_registration_count = random.randint(2, 3)
    user_password = '12345'
    coordinates = [[55.670926, 37.555657], [55.678194, 37.563501], [55.720396, 37.560844], [55.735342, 37.594658],
                   [55.728865, 37.624671], [55.709586, 37.622812], [55.706947, 37.588010], [55.689369, 37.605286]]
    locations = ['Ukraine, Kiev', 'Russia, Moscow', 'Russia, Irkutsk', 'Russia, Ufa', ]
    genres = ['Comedy', 'Horror', 'Romance', 'Action', 'Adventure', 'Western', 'War', 'Thriller', 'Documentary', ]
    start_date = timezone.datetime(timezone.datetime.now().year, timezone.datetime.now().month, 1)
    end_date = timezone.datetime(timezone.datetime.now().year, timezone.datetime.now().month,
                                 calendar.monthrange(timezone.datetime.now().year, timezone.datetime.now().month)[1])
    game_durations = [45, 50, 60, 90, 100, 120, 150, 200, ]

    def handle(self, *args, **options):
        self.create_users()
        self.create_quests()
        self.create_games()
        self.create_coupons()
        self.comment_games()
        self.comment_quests()
        self.subscribe_for_quests()
        self.subscribe_for_users()
        self.register_users_for_game()

    def create_users(self):
        print('Users creation:')
        for i in range(self.users_count):
            user = User.objects.create(
                phone='+7' + str(random.randrange(1000000000, 9999999999)),
                is_active_phone=True,
                username='username_' + str(i + 1),
                first_name='Test ',
                last_name='User ' + str(i + 1),
                birthday_date=self.generate_random_birthday_date(),
                gender=random.choices(['NOT_SET', 'MALE', 'FEMALE'])[0],
                location=random.choices(self.locations)[0],
                reliability=random.randint(0, 100),
            )
            Token.objects.create(user=user)
            user.set_password(self.user_password)
            user.save()
            print('.', end='', flush=True)
        users = User.objects.filter(admin=False)
        self.set_images(users, 'avatars', '{}.jpg', 'profile_image')
        print('\nUsers creation: DONE')

    def create_quests(self):
        print('Quests creation:')
        for i in range(self.quests_count):
            coordinates = random.choices(self.coordinates)[0]
            Quest.objects.create(
                name='Quest_' + str(i + 1),
                phone='+7' + str(random.randrange(1000000000, 9999999999)),
                location=random.choices(self.locations)[0],
                x_coordinate=coordinates[0],
                y_coordinate=coordinates[1],
                rating=random.randint(0, 5),
            )
            print('.', end='', flush=True)
        quests = Quest.objects.all()
        self.set_images(quests, 'quest_photos', 'flag_{}.png', 'photo')
        self.set_images(quests, 'quest_covers', 'quest_{}.jpg', 'cover_image')
        stations = self.get_metro_station_names()
        print('\nMetro stations creation:')
        for quest in quests:
            self.add_gallery_photos(quest)
            for i in range(random.randint(1, 3)):
                MetroStation.objects.create(
                    name=random.choice(stations),
                    color=("#%06x" % random.randint(0, 0xFFFFFF)),
                    quest=quest,
                )
            print('.', end='', flush=True)
        print('\nMetro stations creation: DONE')
        print('Quests creation: DONE')

    def create_games(self):
        print('Games creation:')
        current_date = self.start_date
        quests = Quest.objects.all()
        while current_date < self.end_date:
            for i in range(self.games_count_per_day):
                timespan = datetime.astimezone(current_date +
                                               timezone.timedelta(hours=random.randrange(1, 23),
                                                                  minutes=random.randrange(1, 60),
                                                                  seconds=random.randrange(1, 60)), tz=pytz.utc)
                game = Game.objects.create(
                    title='Game_' + str(i + 1),
                    description=self.make_game_description(current_date, i + 1),
                    genre=random.choices(self.genres)[0],
                    timespan=timespan,
                    duration=random.choices(self.game_durations)[0],
                    quest=random.choices(quests)[0],
                    level=random.choices(['1', '2', '3', '4', '5'])[0],
                    price=random.randrange(100, 999),
                    min_players_count=random.randrange(2, 4),
                    max_players_count=6,
                    cancel=False,
                )
                Team.objects.create(
                    game=game,
                )
                print('.', end='', flush=True)
            current_date += timezone.timedelta(days=1)
        games = Game.objects.all()
        self.set_images(games, 'game_photos', 'fc_{}.jpg', 'photo')
        self.set_images(games, 'game_covers', 'game_{}.jpg', 'cover_image')
        print('\nGames creation: DONE')

    def create_coupons(self):
        print('Coupons creation:')
        for i in range(self.coupons_count):
            Coupon.objects.create(
                code=random.randint(1000000000, 9999999999),
                start_date=timezone.datetime.now().date(),
                end_date=timezone.datetime.now().date() + timezone.timedelta(days=random.randint(1, 50)),
                discount=random.randint(1, 100),
                units=random.choices(['PERCENT', 'RUB'])[0],
                type=random.choices(['INDIVIDUAL', 'GENERAL'])[0],
            )
            print('.', end='', flush=True)
        print('\nCoupons creation: DONE')

    def comment_games(self):
        print('Game comments creation:')
        users = User.objects.filter(admin=False)
        games = Game.objects.all()
        for user in users:
            for i in range(self.comments_count):
                game = random.choices(games)
                GameComment.objects.create(
                    user=user,
                    game=game[0],
                    text='Comment for {} from {}. Cool game!'.format(game[0].title, user.phone),
                )
                print('.', end='', flush=True)
        print('\nGame comments creation: DONE')

    def comment_quests(self):
        print('Quest comments creation:')
        users = User.objects.filter(admin=False)
        quests = Quest.objects.all()
        for user in users:
            for i in range(self.comments_count):
                quest = random.choices(quests)
                QuestComment.objects.create(
                    user=user,
                    quest=quest[0],
                    text='Comment for {} from {}. Cool game!'.format(quest[0].name, user.phone),
                    scores=random.randrange(1, 5),
                )
                print('.', end='', flush=True)
        print('\nQuest comments creation: DONE')

    def subscribe_for_quests(self):
        print('Quest subscriptions creation:')
        users = User.objects.filter(admin=False)
        quests = Quest.objects.all()
        for user in users:
            for i in range(self.subscriptions_count):
                quest = random.choices(quests)[0]
                try:
                    QuestSubscription.objects.get(user=user, quest=quest)
                    continue
                except QuestSubscription.DoesNotExist:
                    QuestSubscription.objects.create(
                        user=user,
                        quest=quest,
                    )
                    print('.', end='', flush=True)
        print('\nQuest subscriptions creation: DONE')

    def subscribe_for_users(self):
        print('User subscriptions creation:')
        users = User.objects.filter(admin=False)
        for user in users:
            for i in range(self.subscriptions_count):
                subscriber = random.choices(users)[0]
                if subscriber != user:
                    try:
                        UserSubscription.objects.get(user=user, subscriber=subscriber)
                        continue
                    except UserSubscription.DoesNotExist:
                        UserSubscription.objects.create(
                            user=user,
                            subscriber=subscriber,
                        )
                        print('.', end='', flush=True)
        print('\nUser subscriptions creation: DONE')

    def register_users_for_game(self):
        print('Register user for a games:')
        users = User.objects.filter(admin=False)
        games = Game.objects.all()
        for user in users:
            for i in range(self.game_registration_count):
                game = random.choices(games)
                teams = Team.objects.filter(game=game[0])
                try:
                    UserInTeam.objects.get(game=game[0], user=user)
                    UserInTeam.objects.create(
                        game=game[0],
                        user=user,
                        team=random.choices(teams)[0],
                        title=user.username + '`s friend',
                        payment=None,
                    )
                except UserInTeam.DoesNotExist:
                    UserInTeam.objects.create(
                        game=game[0],
                        user=user,
                        team=random.choices(teams)[0],
                        title=user.username,
                        payment=None,
                    )
                    game[0].players_count += 1
                    game[0].save()
                    print('.', end='', flush=True)
        print('\nRegister user for a games: DONE')

    @staticmethod
    def add_gallery_photos(quest):
        for i in range(5):
            image = QuestImage.objects.create(quest=quest)
            file_name = f'gallery_{i}.png'
            with open(os.path.join('test_data', 'images', 'gallery_photos', file_name), 'rb') as f:
                field = getattr(image, 'image')
                field.save(file_name, File(f))

    @staticmethod
    def generate_random_birthday_date():
        str_date = f'{random.randrange(gmtime(0).tm_year, datetime.now().year)}-' \
                   f'{random.randrange(1, 12)}-' \
                   f'{random.randrange(1, 31)}'
        try:
            return datetime.strptime(str_date, '%Y-%m-%d').date()
        except ValueError:
            return None

    @staticmethod
    def set_images(objects, folder, file_template, field_name):
        images_count = len(os.listdir(os.path.join('test_data', 'images', folder)))
        i = 1
        for obj in objects:
            file_name = file_template.format(i)
            with open(os.path.join('test_data', 'images', folder, file_name), 'rb') as f:
                field = getattr(obj, field_name)
                field.save(file_name, File(f))
            i += 1
            if i > images_count:
                i = 1

    @staticmethod
    def get_metro_station_names():
        filename = os.path.join('test_data', 'text', 'Moscow_metro_stations.txt')
        stations = []
        with open(filename, 'r') as f:
            for line in f:
                text = line.strip()
                if text != '':
                    stations.append(text)
        return stations

    @staticmethod
    def make_game_description(dt, number):
        return f"""# Game #{number}
## Date: {dt.strftime('%d %B')}
### Заголовок 3
#### Заголовок 4
##### Заголовок 5
###### Заголовок 6
Стандартными положениями являются:
* Начальный __удар__. Наносится в начале _каждого тайма_, а также — после каждого забитого мяча. Назначается с центральной точки поля (в центральном круге).
* Вбрасывание мяча (аут). Бросается руками из-за боковой линии. Назначается после того, как мяч эту самую боковую линию пересёк. При этом аут бросает соперник игрока, которого мяч коснулся последним перед уходом за боковую линию
* Удар от ворот. Наносится вратарём, после того, как мяч полностью пересёк линию ворот (вне территории ворот) от игрока нападавшей команды
* Угловой удар. Наносится игроком нападающей команды из углового сектора. Назначается в случае, если мяч полностью пересекает линию ворот"""
