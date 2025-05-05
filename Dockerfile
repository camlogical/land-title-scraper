# Start with a minimal Python image
FROM python:3.12-slim-buster

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    curl \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libx11-xcb1 \
    libfontconfig \
    libxcomposite1 \
    libxrandr2 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libxss1 \
    libxtst6 \
    libappindicator3-1 \
    libatspi2.0-0 \
    libdrm2 \
    libxv1 \
    xdg-utils \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Set the working directory for the app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files into the container
COPY . .

# Install Playwright and its dependencies
RUN python -m playwright install --with-deps

# Expose the port the app will run on
EXPOSE 8080

# Command to run the app using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
