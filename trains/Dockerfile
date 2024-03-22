FROM python:3.9-slim
WORKDIR /app
COPY trains .
COPY common ./common
RUN pip install pdm
RUN pdm install
ENV CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672/
ENV PYTHONPATH=src/trains
