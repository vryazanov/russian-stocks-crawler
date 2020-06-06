FROM python:3.8.2-slim as base

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /srv/app
COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root
