FROM python:3.11-slim

WORKDIR /usr/src/app/api

COPY requirements.txt /usr/src/app/api/requirements.txt

RUN pip install -r /usr/src/app/api/requirements.txt --pre

COPY . /usr/src/app/api
