#!/bin/bash

alembic upgrade head

export PYTHONUNBUFFERED=1

# Запуск Gunicorn с оптимизированными параметрами
gunicorn src.api_app:app \
    -w 3 \
    -k uvicorn.workers.UvicornWorker \
    --threads 2 \
    --timeout 30 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --bind 0.0.0.0:8000
