from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from database.models import Base


async def create_tables(engine: AsyncEngine):
    """
    Create database tables
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_engine() -> AsyncEngine:
    return create_async_engine(
        url=URL.create(
            "postgresql+asyncpg",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
        ),
        future=True,
        echo=True,
    )


def create_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
