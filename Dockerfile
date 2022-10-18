FROM python:3-alpine

WORKDIR /usr/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src/requirements.txt /usr/requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /usr/requirements.txt

COPY . /usr/

