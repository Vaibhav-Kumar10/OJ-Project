FROM python:3.9-slim

# Install gcc, g++, openjdk, and other dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache django markdown dotenv google-genai 


EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=oj.settings
ENV PYTHONUNBUFFERED=1

# RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# RUN pip install --no-cache django markdown dotenv google-genai gunicorn psycopg2-binary dj-database-url whitenoise
# CMD ["gunicorn", "oj.wsgi:application", "--bind", "0.0.0.0:8000"]
