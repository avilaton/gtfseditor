FROM ubuntu:latest
MAINTAINER Gastón Avila "avila.gas@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libpq-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD manage.py runserver