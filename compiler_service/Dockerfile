FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install compilers
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create isolated user
RUN useradd -m -u 1000 compileruser

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ownership
RUN chown -R compileruser:compileruser /app

USER compileruser

EXPOSE 8001

CMD ["gunicorn", "compiler_service.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2", "--threads", "2", "--timeout", "15"]