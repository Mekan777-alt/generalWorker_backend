FROM python:3.10-slim-bullseye AS builder

# Устанавливаем необходимые пакеты для локалей
RUN apt-get update && apt-get install -y locales && \
    locale-gen ru_RU.UTF-8 && \
    update-locale LANG=ru_RU.UTF-8 && \
    apt-get clean

# Устанавливаем переменные окружения для локали
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8

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