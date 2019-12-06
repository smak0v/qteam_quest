FROM python:3.7-alpine

RUN apk update && apk add build-base postgresql postgresql-dev libpq jpeg-dev zlib-dev

RUN mkdir /usr/src/korobka_games

WORKDIR /usr/src/korobka_games

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONBUFFERED 1

COPY . .