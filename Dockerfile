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
COPY ./pyproject.toml /src/pyproject.toml
COPY ./poetry.lock /src/poetry.lock
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# copy project
COPY ./src /app/src/
