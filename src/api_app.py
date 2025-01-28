from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi import FastAPI
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from sqlalchemy import select

from models.enums import RolesEnum
from models.entity import RoleModel
from database.session import async_session_maker

from api.controllers.auth_controller import router as auth_router
from api.controllers.user_controller import router as user_router
from api.controllers.tasks_controller import router as tasks_router
from api.controllers.subscription_controller import router as subscription_router
from api.controllers.faq_controller import router as faq_router



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Инициализация Redis
    redis = aioredis.from_url(
        url=f"redis://{settings.redis_settings.host}:{settings.redis_settings.port}",
        encoding="utf-8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    async with async_session_maker() as session:
        for role in RolesEnum:
            result = await session.execute(select(RoleModel).where(RoleModel.name == role.value))
            db_role = result.scalar()
            if not db_role:

                role_instance = RoleModel(name=role.value)
                session.add(role_instance)

        await session.commit()

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

app.include_router(user_router)
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(subscription_router)
app.include_router(faq_router)