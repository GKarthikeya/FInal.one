FROM python:3.10-slim

# Chrome install
RUN apt-get update && apt-get install -y wget gnupg unzip curl \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Working dir
WORKDIR /app

# Copy files
COPY . .

# Install deps
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV GOOGLE_CHROME_BIN=/usr/bin/google-chrome

CMD ["./start.sh"]
