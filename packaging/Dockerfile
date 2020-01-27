FROM python:3.7-alpine

RUN apk update && apk add build-base postgresql postgresql-dev libpq jpeg-dev zlib-dev

ENV PYTHONUNBUFFERED 1

COPY packaging/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /src/

COPY packaging/entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh

WORKDIR /src

ENV DJANGO_SETTINGS_MODULE=qteam_quest.settings

EXPOSE 8000

EXPOSE 443

ENTRYPOINT ['/entrypoint.sh']
