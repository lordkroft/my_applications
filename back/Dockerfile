# syntax=docker/dockerfile:1

FROM python:3.6.8-alpine3.9

RUN apk add --no-cache nginx 

WORKDIR /code

COPY ./code/backend.py /code/backend.py


#WORKDIR /var/www/

#ADD . /var/www/

ADD . /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./nginx-conf/nginx-back.conf /etc/nginx/sites-available/default

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

