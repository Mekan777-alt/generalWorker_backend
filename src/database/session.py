from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import settings

# Настройка пула соединений
engine = create_async_engine(
    settings.database_settings.uri,
    pool_size=100,  # Размер пула соединений
    max_overflow=200,  # Дополнительные соединения сверх пула
    pool_timeout=30,  # Таймаут ожидания получения соединения из пула
    pool_recycle=30  # Закрытие неактивных соединений каждые 30 секунд
)


async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """
    Генератор сессии
    :return: Возвращает асинхронную сессию
    """
    async with async_session_maker() as session:
        yield session
