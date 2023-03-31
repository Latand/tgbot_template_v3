FROM python:3.11-slim
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME}"

COPY ./infrastructure/webhook/requirements.txt /usr/src/app/"${BOT_NAME}"/requirements.txt
RUN pip install -r /usr/src/app/"${BOT_NAME}"/requirements.txt --pre

COPY . /usr/src/app/"${BOT_NAME}"