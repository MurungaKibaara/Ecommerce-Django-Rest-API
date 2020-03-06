FROM python:latest
ENV LANG C.UTF-8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


MAINTAINER Murunga Kibaara "murungaephantus@gmail.com"

RUN mkdir /eretail

COPY /eretail/ /eretail

RUN apt-get -y update
RUN apt-get install -y python python-pip python-dev python-psycopg2 postgresql-client

ADD requirements.txt /eretail/requirements.txt
RUN pip install -r /eretail/requirements.txt

RUN apt-get -y update && apt-get -y autoremove

EXPOSE 9000

CMD gunicorn -b :9000 core.wsgi
