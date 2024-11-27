FROM python:3.10-slim-bullseye AS builder

# Устанавливаем зависимости для локалей
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales && \
    rm -rf /var/lib/apt/lists/*

# Генерация локалей
RUN echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ru_RU.UTF-8

# Устанавливаем переменные окружения для локалей
ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_ALL=ru_RU.UTF-8

WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Устанавливаем права на выполнение скриптов
RUN chmod +x utils/start_*.sh

# Устанавливаем путь для Python
ENV PYTHONPATH="/app/src"