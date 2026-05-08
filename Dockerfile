FROM python:3.12-slim

RUN  apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry lock --no-update || true
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .
RUN mkdir -p /app/logs && chmod 755 /app/logs

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

