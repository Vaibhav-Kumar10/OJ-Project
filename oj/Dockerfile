FROM python:3.9-slim

# Install gcc, g++, openjdk, and other dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

COPY . /app

RUN pip install --no-cache django
RUN pip install --no-cache markdown
RUN pip install --no-cache dotenv
RUN pip install --no-cache google-genai
RUN pip install --no-cache psycopg2

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=oj.settings
ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]