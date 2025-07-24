#!/bin/bash

apt-get update
apt-get install -y wget unzip

# Install Chrome (stable version)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

pip install -r requirements.txt
