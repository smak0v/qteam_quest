import json
import sys
import requests


def set_headers(token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token,
    }
    return headers


def reset_headers():
    return {'Content-Type': 'application/json'}


if len(sys.argv) == 2:
    port = sys.argv[1]
else:
    port = '8000'

# ENDPOINT = 'http://176.113.81.212:80/'
ENDPOINT = f'http://localhost:{port}/'
HEADERS = reset_headers()

games = requests.get(ENDPOINT + 'api/quests/').json()
venues = requests.get(ENDPOINT + 'api/venues/').json()
users = requests.get(ENDPOINT + 'api/users/').json()

print("Deleting quests and all related objects")
for game in games:
    requests.delete(ENDPOINT + 'api/quests/{}/'.format(int(game['id'])))
    print('.', end='', flush=True)
print()

print("Deleting venues and all related objects")
for venue in venues:
    response = requests.delete(ENDPOINT + 'api/venues/{}/'.format(int(venue['id'])))
    print('.', end='', flush=True)
print()

print("Deleting test users")
for user in users:
    if user['admin']:
        continue

    if not user['username'].startswith("test_user_"):
        continue

    login_data = {
        'username': user['username'],
        'password': 'secret_password_{}'.format(int(user['last_name'].split(' ')[-1])),
    }
    HEADERS = reset_headers()
    login_response = requests.post(ENDPOINT + 'api/users/login/', data=json.dumps(login_data), headers=HEADERS)
    token = login_response.json()['key']
    HEADERS = set_headers(token)
    response = requests.delete(ENDPOINT + 'api/users/{}/'.format(int(user['id'])), headers=HEADERS)
    print('.', end='', flush=True)
print()
