FROM ubuntu:latest
MAINTAINER Alexander Mamaev "alxmamaev@ya.ru"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "app:app" "-b", "0.0.0.0:8000"]