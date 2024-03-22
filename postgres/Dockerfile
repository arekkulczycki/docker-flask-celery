FROM postgres:alpine

ENV POSTGRES_USER micro-train
ENV POSTGRES_PASSWORD micro-train
ENV POSTGRES_DB micro-train

COPY postgres/init.sql /docker-entrypoint-initdb.d/
