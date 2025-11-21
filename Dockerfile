FROM python:3.13-alpine

WORKDIR /usr/library-main

ENV PYTHONUNBUFFERED=1 \
    TZ="Europe/Moscow"

RUN apk add --no-cache \
    curl \
    postgresql-dev \
    graphviz \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev

RUN pip install --upgrade pip --no-cache-dir && \
    pip install poetry==2.2.1 --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-cache --without dev --no-root

COPY . .
