# base image
FROM python:3.11.3-slim-bullseye

# set working directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc python3-dev

# install python dependencies
RUN pip install --upgrade pip
# copy poetry.lock and pyproject.toml
COPY ../pyproject.toml ../poetry.lock /src/
RUN pip install poetry
# install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# copy project
COPY ./src /src/

