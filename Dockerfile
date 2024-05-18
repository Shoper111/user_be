FROM python:3.11.6-bullseye as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

RUN apt-get update && apt-get install -y curl git gcc -y

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$POETRY_HOME/bin:$PATH

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY user_be/ ./user_be
COPY server.py ./server.py
COPY docker-entrypoint.sh ./entrypoint.sh

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-ansi


RUN groupadd -r comp && useradd --no-log-init -r -g comp comp
USER comp

CMD ["sh", "entrypoint.sh"]
