FROM python:3.9-slim
WORKDIR /app
COPY gatekeeper .
COPY common ./common

RUN pip install pdm
RUN pdm install

RUN groupadd app && useradd -g app app
RUN chown -R app:app /app
USER app

EXPOSE 5000
ENV PYTHONPATH=src/gatekeeper
