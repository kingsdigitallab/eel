# syntax=docker/dockerfile:1
FROM python:2.7.18-alpine
ENV PYTHONUNBUFFERED=1
RUN apk add build-base postgresql-dev jpeg-dev zlib-dev libxslt-dev
WORKDIR /eel
COPY requirements.txt .
# https://stackoverflow.com/a/55101589
RUN pip install --no-binary Django -r requirements.txt
