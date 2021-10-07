# syntax=docker/dockerfile:1
FROM python:2.7.18-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
