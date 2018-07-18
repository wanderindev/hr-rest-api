FROM python:3.7.0-alpine3.8

MAINTAINER Javier Feliu <javier@feliu.io>

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

ENV INSTALL_PATH /rest-api
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup -S rest && adduser -S -g rest rest
USER rest

CMD gunicorn -b 0.0.0.0:5001 --access-logfile - --reload "run:app"