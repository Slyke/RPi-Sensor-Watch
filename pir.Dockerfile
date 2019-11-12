FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN apk add --no-cache -Uu --virtual .build-dependencies python3-dev libffi-dev openssl-dev build-base musl python-dev
RUN pip3 install --no-cache --upgrade pyserial RPi.GPIO
RUN apk del --purge .build-dependencies
RUN apk add --no-cache --purge curl ca-certificates musl wiringpi
RUN rm -rf /var/cache/apk/* /tmp/*
RUN pip3 install --upgrade requests
RUN pip3 install gpiozero

COPY pir.py .

CMD ["python", "pir.py"]
