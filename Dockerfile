FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential

ARG APP_DIR="/opt/app/"

COPY . "$APP_DIR"
WORKDIR "$APP_DIR"

ENV AWS_ACCESS_KEY ""
ENV AWS_ACCESS_KEY_ID ""
ENV MONGO_URL ""
ENV S3_BUCKET ""
ENV S3_URL ""
ENV SECRET_SERVICE_KEY ""

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8080", "app:app"]