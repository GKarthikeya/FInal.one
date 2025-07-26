FROM python:3.10-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y wget gnupg unzip curl xvfb chromium chromium-driver

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set work directory
WORKDIR /app

# Copy all files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Render
EXPOSE 10000

# Default start command (can be overridden by startCommand in Render)
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:10000", "grok.app:app"]
