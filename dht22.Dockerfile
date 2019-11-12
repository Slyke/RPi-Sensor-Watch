FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN apk add --no-cache -Uu --virtual .build-dependencies libffi-dev openssl-dev build-base python3-dev python-dev
RUN pip3 install --upgrade requests
RUN pip3 install --upgrade Adafruit_DHT

COPY dht22.py .

CMD ["python", "dht22.py"]
