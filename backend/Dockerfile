# syntax=docker/dockerfile:1

FROM python:3.6.8-alpine3.9

WORKDIR /var/www/

COPY backend/backend.py /var/www/backend.py

#ADD . /var/www/

#ADD . /code

COPY . /var/www/

ADD backend/wsgi.py /var/www/

RUN python -m pip install --upgrade pip

RUN pip install -r backend/requirements.txt

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

