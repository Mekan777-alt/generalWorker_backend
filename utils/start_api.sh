#!/bin/bash

alembic upgrade head

export PYTHONUNBUFFERED=1

uvicorn src.api_app:app --host 0.0.0.0 --port 8000
