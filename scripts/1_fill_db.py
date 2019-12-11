import json
import random
import os
import requests
import sys
from django.utils import timezone


def set_headers(auth_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + auth_token,
    }
    return headers


def reset_headers():
    return {'Content-Type': 'application/json'}


def make_game_description(dt, number):
    return f"""
# Game #{number}
## Date: {dt.strftime('%d %B')}
### Заголовок 3
#### Заголовок 4
##### Заголовок 5
###### Заголовок 6
Стандартными положениями являются: 
* Начальный __удар__. Наносится в начале _каждого тайма_, а также — после каждого забитого мяча. Назначается с 
центральной точки поля (в центральном круге). 
* Вбрасывание мяча (аут). Бросается руками из-за боковой линии. Назначается после того, как мяч эту самую боковую 
линию пересёк. При этом аут бросает соперник игрока, которого мяч коснулся последним перед уходом за боковую линию 
* Удар от ворот. Наносится вратарём, после того, как мяч полностью пересёк линию ворот (вне территории ворот) от 
игрока нападавшей команды 
* Угловой удар. Наносится игроком нападающей команды из углового сектора. Назначается в случае, если мяч полностью 
пересекает линию ворот 
""".strip()


if len(sys.argv) == 2:
    port = sys.argv[1]
else:
    port = '8000'

# ENDPOINT = 'http://176.113.81.212:80/'
ENDPOINT = f'http://localhost:{port}/'
HEADERS = reset_headers()
USERS_COUNT = 100
VENUES_COUNT = 5
VENUE_LOCATIONS = ['Ukraine, Kiev', 'Russia, Moscow', 'Russia, Irkutsk', 'Russia, Ufa', ]
GAMES_START_DT = timezone.datetime(2019, 11, 1)
GAMES_END_DT = timezone.datetime(2019, 12, 1)
GAMES_PER_DAY_COUNT = 5
GAMES_DURATIONS = [45, 50, 60, 90, 100, 120, 150, 200, ]
COMMENTS_COUNT_PER_USER = 10
SUBSCRIPTIONS_COUNT_PER_USER = 5
USER_GAME_REGISTRATION_LIMIT = 10
USER_GAME_RESERVATION_PLACES_LIMIT = 20
script_dir = os.path.dirname(os.path.abspath(__file__))

users = requests.get(ENDPOINT + 'api/users/').json()
test_users = [user for user in users if user['username'].startswith('test_user')]
need_create_users = len(test_users) == 0

if need_create_users:
    print("Users registration")
    for i in range(USERS_COUNT):
        user = {
            'username': 'test_user_{}'.format(str(i + 1)),
            'first_name': 'Test',
            'last_name': 'User {}'.format(str(i + 1)),
            'email': 'test_user_email_{}@gmail.com'.format(str(i + 1)),
            'password1': 'secret_password_{}'.format(str(i + 1)),
            'password2': 'secret_password_{}'.format(str(i + 1)),
        }
        requests.post(ENDPOINT + 'api/users/register/', data=json.dumps(user), headers=HEADERS)
        print('.', end='', flush=True)
    print()
else:
    print(f'There is already {len(test_users)} test users. Run 0_clear_db.py if you want to delete them!')

venues = requests.get(ENDPOINT + 'api/venues/').json()
if len(venues) == 0:
    print("Venues creation")
    for i in range(VENUES_COUNT):
        venue = {
            'name': 'Venue {}'.format(str(i + 1)),
            'location': random.choices(VENUE_LOCATIONS)[0],
            'x_coordinate': 21.34564,
            'y_coordinate': 45.25431,
        }
        response = requests.post(ENDPOINT + 'api/venues/', data=json.dumps(venue), headers=HEADERS)

    venues = requests.get(ENDPOINT + 'api/venues/').json()
else:
    print(f'There is already {len(venues)} venues. Run 0_clear_db.py if you want to delete them!')

print("Games creation")
current_dt = GAMES_START_DT
while current_dt < GAMES_END_DT:
    current_date = current_dt.strftime('%Y-%m-%d')
    current_games = requests.get(f'{ENDPOINT}api/quests/?date={current_date}').json()
    if len(current_games) == 0:
        for i in range(GAMES_PER_DAY_COUNT):
            game = {
                'title': 'Game {}'.format(str(i + 1)),
                'description': make_game_description(current_dt, i + 1),
                'timespan': (current_dt + timezone.timedelta(hours=random.randrange(1, 23),
                                                             minutes=random.randrange(1, 60),
                                                             seconds=random.randrange(1, 60))).__str__(),
                'duration': random.choices(GAMES_DURATIONS)[0],
                'price': random.randrange(100, 999),
                'venue': int(random.choices(venues)[0]['id']),
                'game_status': random.choices(['PUBLIC', 'PRIVATE', ])[0],
                'a_side_players_count': random.randrange(5, 11),
                'cancel': (i + 1) % 3 == 0,
            }
            requests.post(ENDPOINT + 'api/quests/', data=json.dumps(game), headers=HEADERS)
            print('.', end='', flush=True)
    else:
        print(f'There is already {len(current_games)} quests for {current_date}.'
              f' Run 0_clear_db.py if you want to delete them!')
    current_dt += timezone.timedelta(days=1)
print()

if need_create_users:
    users = requests.get(ENDPOINT + 'api/users/').json()
    games = requests.get(ENDPOINT + 'api/quests/').json()

    print("Users actions")
    for user in users:
        if user['admin']:
            continue

        username = user['username']
        if not username.startswith("test_user_"):
            continue

        login_data = {
            'username': username,
            'password': 'secret_password_{}'.format(int(user['last_name'].split(' ')[-1])),
        }
        HEADERS = reset_headers()
        response = requests.post(ENDPOINT + 'api/users/login/', data=json.dumps(login_data), headers=HEADERS)
        token = response.json()['key']
        HEADERS = set_headers(token)

        # Games commenting
        for i in range(COMMENTS_COUNT_PER_USER):
            game = random.choices(games)
            comment_for_game = {
                'user': int(user['id']),
                'game': int(game[0]['id']),
                'text': 'Comment for {} from {}. Cool game!'.format(game[0]['title'], username)
            }
            comment_response = requests.post(ENDPOINT + 'api/quests/{}/comments/'.format(int(game[0]['id'])),
                                             data=json.dumps(comment_for_game), headers=HEADERS)

        # Venues commenting
        for i in range(COMMENTS_COUNT_PER_USER):
            venue = random.choices(venues)
            comment_for_venue = {
                'venue': int(venue[0]['id']),
                'user': int(user['id']),
                'text': 'Comment for {} from {}. Cool game!'.format(venue[0]['name'], username),
                'scores': random.randrange(1, 5),
            }
            comment_response = requests.post(ENDPOINT + 'api/venues/{}/comments/'.format(int(venue[0]['id'])),
                                             data=json.dumps(comment_for_venue), headers=HEADERS)

        # Subscribing for a venue
        for i in range(SUBSCRIPTIONS_COUNT_PER_USER):
            venue = random.choices(venues)
            venue_subscription = {
                'venue': int(venue[0]['id']),
                'user': int(user['id']),
            }
            subscription_response = requests.post(ENDPOINT + 'api/venues/{}/subscribe/'.format(int(venue[0]['id'])),
                                                  data=json.dumps(venue_subscription), headers=HEADERS)

        # Subscribing for a user
        for i in range(SUBSCRIPTIONS_COUNT_PER_USER):
            user_for_subscribing = random.choices(users)
            user_subscription = {
                'user': int(user['id']),
                'subscriber': int(user_for_subscribing[0]['id']),
            }
            subscription_response = requests.post(ENDPOINT + 'api/users/{}/subscribe/'.format(int(user['id'])),
                                                  data=json.dumps(user_subscription), headers=HEADERS)

        # Register user for a game
        for i in range(USER_GAME_REGISTRATION_LIMIT):
            game = random.choices(games)
            game_teams = requests.get(ENDPOINT + 'api/quests/{}/teams/'.format(int(game[0]['id']))).json()
            user_in_team = {
                'game': int(game[0]['id']),
                'user': int(user['id']),
                'team': int(random.choices(game_teams)[0]['id']),
                'user_position': random.choices(['GOALIE', 'DEFENDER', 'MIDFIELDER', 'FORWARD'])[0]
            }
            game_registration_response = requests.post(ENDPOINT + 'api/quests/{}/players/'.format(int(game[0]['id'])),
                                                       data=json.dumps(user_in_team), headers=HEADERS)

        # Reservation places for a game
        for i in range(random.randrange(1, USER_GAME_RESERVATION_PLACES_LIMIT)):
            game = random.choices(games)
            game_teams = requests.get(ENDPOINT + 'api/quests/{}/teams/'.format(int(game[0]['id']))).json()
            reserved_place_in_team = {
                'title': '{}`s friend'.format(username),
                'game': int(game[0]['id']),
                'user': int(user['id']),
                'team': int(random.choices(game_teams)[0]['id']),
                'reserved_position': random.choices(['GOALIE', 'DEFENDER', 'MIDFIELDER', 'FORWARD'])[0]
            }
            game_place_reservation_response = requests.post(
                ENDPOINT + 'api/quests/{}/reserved_places/'.format(int(game[0]['id'])),
                data=json.dumps(reserved_place_in_team),
                headers=HEADERS,
            )

        logout_response = requests.get(ENDPOINT + 'api/users/logout/')
        reset_headers()
        print(".", end='', flush=True)
    print()
else:
    print('No need to perform users actions because no users has been created!')
