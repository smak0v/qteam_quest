FROM python:3.7-alpine

RUN apk update && apk add build-base postgresql postgresql-dev libpq jpeg-dev zlib-dev

RUN mkdir /usr/src/qteam_quest

WORKDIR /usr/src/qteam_quest

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONBUFFERED 1

COPY . .