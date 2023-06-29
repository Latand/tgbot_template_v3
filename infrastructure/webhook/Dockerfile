FROM python:3.11-slim
ENV WEBHOOK_APP_NAME=webhook

WORKDIR /usr/src/app/$WEBHOOK_APP_NAME

COPY ./infrastructure/webhook/requirements.txt /usr/src/app/$WEBHOOK_APP_NAME/requirements.txt
RUN pip install -r /usr/src/app/$WEBHOOK_APP_NAME/requirements.txt --pre

COPY . /usr/src/app/$WEBHOOK_APP_NAME