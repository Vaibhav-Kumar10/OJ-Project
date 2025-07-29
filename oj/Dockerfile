FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app code
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir \
    django \
    markdown \
    python-dotenv \
    google-genai \
    psycopg2-binary \
    dj-database-url \
    whitenoise \
    gunicorn

# Expose port
EXPOSE 8000

# Set env vars
ENV DJANGO_SETTINGS_MODULE=oj.settings
ENV PYTHONUNBUFFERED=1

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn oj.wsgi:application --bind 0.0.0.0:8000"]
