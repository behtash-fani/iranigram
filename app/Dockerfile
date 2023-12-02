FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt