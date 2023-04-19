# base image
FROM python:3.11.3-slim-bullseye

# set working directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc python3-dev libpq5 

# install python dependencies
RUN pip install --upgrade pip
# copy poetry.lock and pyproject.toml
COPY ../pyproject.toml ../poetry.lock /src/
RUN pip install poetry
# install project dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev && \
    apt-get remove -y libpq-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# copy project
COPY ./src /src/


