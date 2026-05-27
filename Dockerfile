FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from project root
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django app from oj/ folder
COPY oj/ .

EXPOSE 8000

CMD ["gunicorn", "oj.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
