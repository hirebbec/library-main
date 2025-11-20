FROM python:3.13-alpine

WORKDIR /usr/library-map/src

ENV PYTHONUNBUFFERED=1 \
    TZ="Europe/Moscow"

RUN apk add curl postgresql-dev graphviz --no-cache && \
    pip install --upgrade pip --no-cache-dir && \
    pip install poetry==2.0.1 --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-cache --without dev

COPY . .
