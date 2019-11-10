#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
apt install -y docker-compose