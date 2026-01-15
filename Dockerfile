FROM python:3.12-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.0

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
RUN cat pyproject.toml
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .