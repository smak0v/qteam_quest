#!/bin/bash

function postgres_ready() {
  python <<END
import sys
import psycopg2
import environ

try:
    ROOT_DIR = environ.Path(__file__) - 3
    APPS_DIR = ROOT_DIR.path('src')
    ENV_PATH = str(APPS_DIR.path('.env'))
    env = environ.Env()
    if env.bool('READ_ENVFILE', default=True):
        env.read_env(ENV_PATH)
    conn = psycopg2.connect(
        dbname=env('POSTGRES_DB_NAME', default=''),
        user=env('POSTGRES_DB_USER', default=''),
        password=env('POSTGRES_DB_PASSWORD', default=''),
        host='postgres')
except psycopg2.OperationalError:
    sys.exit(-1)
    sys.exit(0)
END
}

until postgres_ready; do
  echo >&2 "Waiting Postgres Service..."
  sleep 1
done
echo "Postgres is Ready.. Let's go!"

python /src/manage.py migrate --noinput

cd /src

daphne -e ssl:443:privateKey=privatekey.pem:certKey=fullchain.pem -u /tmp/daphne.sock -p 8000 qteam_quest.asgi:application -b 0.0.0.0
