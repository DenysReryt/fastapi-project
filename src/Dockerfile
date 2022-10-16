FROM python:3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /usr/src/app/requirements.txt

COPY . /usr/src/app/