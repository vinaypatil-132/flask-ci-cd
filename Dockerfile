# Use slim Python base
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Create data folder and ensure permissions
RUN mkdir -p /app/data && chown -R nobody:nogroup /app/data

# Expose port 80 (container)
EXPOSE 80

# Run app using Gunicorn (production)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app", "--workers", "3", "--threads", "2", "--timeout", "120"]
