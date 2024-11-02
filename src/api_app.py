import firebase_admin

from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from firebase_admin import credentials
from redis import asyncio as aioredis
from fastapi import FastAPI
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Инициализация Redis
    redis = aioredis.from_url(
        url=f"redis://{settings.redis_settings.host}:{settings.redis_settings.port}",
        username=settings.redis_settings.username,
        password=settings.redis_settings.password,
        encoding="utf-8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    cred = credentials.Certificate("src/generalworker-ee270-firebase-adminsdk-b3xb3-d5c5a122f0.json")
    firebase_admin.initialize_app(cred)

    yield

# Определяем middleware и создаем приложение FastAPI
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]

app = FastAPI(
    lifespan=lifespan,
    title="generalWorkers API",
    version="0.0.1",
    docs_url="/docs",
    root_path="/api",
    middleware=middleware,
)

