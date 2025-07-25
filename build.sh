#!/usr/bin/env bash

set -e  # Exit on any error

echo "🔧 Updating packages and installing dependencies..."
apt-get update && apt-get install -y wget unzip curl gnupg2 lsb-release

echo "🌐 Adding Google Chrome repository..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

echo "📦 Installing Google Chrome..."
apt-get update && apt-get install -y google-chrome-stable

# Get the installed Chrome version
CHROME_VERSION=$(google-chrome-stable --version | grep -oP '\d+\.\d+\.\d+')
echo "🔍 Installed Chrome version: $CHROME_VERSION"

# Get the corresponding Chromedriver version
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION" || true)

# Fallback if exact match not found
if [ -z "$CHROMEDRIVER_VERSION" ]; then
    echo "⚠️ Exact Chromedriver version for $CHROME_VERSION not found, using latest instead..."
    CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
fi

echo "📥 Downloading Chromedriver version: $CHROMEDRIVER_VERSION"
wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"

echo "📦 Installing Chromedriver..."
unzip -o /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

echo "✅ Chrome and Chromedriver setup complete."
