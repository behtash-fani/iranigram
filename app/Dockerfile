FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin


RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

CMD python manage.py makemigrations --noinput && \
    while ! python manage.py migrate --noinput  ; do sleep 1 ; done && \
    python manage.py collectstatic --noinput && \
    python manage.py createsuperuser --phone_number 09302521022 --noinput;