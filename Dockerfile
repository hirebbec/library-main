FROM python:3.13-slim

WORKDIR /usr/library-main

ENV PYTHONUNBUFFERED=1 \
    TZ="Europe/Moscow"

RUN apt update && apt install -y --no-install-recommends \
    ca-certificates \
    curl \
    libpq-dev \
    graphviz \
    gcc \
    g++ \
    build-essential \
    libffi-dev \
    openssl \
    git \
    && apt clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --no-cache-dir && \
    pip install poetry==2.2.1 --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-cache --without dev --no-root

COPY . .
