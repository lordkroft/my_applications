# syntax=docker/dockerfile:1

FROM python:3.6.8-alpine3.9

#WORKDIR /code

#COPY ./code/backend.py /code/backend.py

WORKDIR /var/www/

ADD . /var/www/

#ADD . /code

COPY . /var/www/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

