FROM python:3.10-slim

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements from project root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django app from oj/ folder
COPY oj/ .

EXPOSE 8000

CMD ["gunicorn", "oj.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]




# FROM python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Copy app code
# COPY . /app

# # Upgrade pip and install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip
# RUN pip install --no-cache-dir django \
#     markdown \
#     python-dotenv \
#     google-genai \
#     psycopg2-binary \
#     dj-database-url \
#     whitenoise \
#     gunicorn

# # Expose port
# EXPOSE 8080

# # Set env vars
# ENV DJANGO_SETTINGS_MODULE=oj.settings
# ENV PYTHONUNBUFFERED=1

# # Run migrations and start Gunicorn
# CMD ["sh", "-c", "python manage.py migrate && gunicorn oj.wsgi:application --bind 0.0.0.0:$PORT"]
