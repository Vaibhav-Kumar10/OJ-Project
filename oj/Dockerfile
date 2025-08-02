FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy app code
COPY . /app

# Upgrade pip and install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip
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
EXPOSE 8080

# Set env vars
ENV DJANGO_SETTINGS_MODULE=oj.settings
ENV PYTHONUNBUFFERED=1

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn oj.wsgi:application --bind 0.0.0.0:$PORT"]
