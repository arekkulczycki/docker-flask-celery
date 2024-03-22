FROM python:3.9-slim
WORKDIR /app
COPY controller .
COPY common ./common

RUN pip install pdm
RUN pdm install

RUN useradd -ms /bin/bash celery
RUN chown -R celery:celery /app
USER celery

ENV CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672/
ENV C_FORCE_ROOT=false
ENV PYTHONPATH=src/controller
