# Use official slim Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies and Chromium
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 \
    libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils libu2f-udev \
    libvulkan1 chromium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variable for Chrome binary path
ENV GOOGLE_CHROME_BIN=/usr/bin/chromium

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app
WORKDIR /app

# Expose the port your app runs on
EXPOSE 10000

# Start the Flask app
CMD ["python", "app.py"]
