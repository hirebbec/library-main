import functools
from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


@functools.lru_cache
def get_engine(url: str | URL, **kwargs) -> AsyncEngine:
    return create_async_engine(url, echo=False, future=True, **kwargs)


def get_async_session(url: str | URL) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(url), expire_on_commit=False)


async def get_session(
    url: str | URL | None = None,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = get_async_session(url=url or settings().postgres_dsn)
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def get_base_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session(url=settings().postgres_dsn):
        yield session


async def get_readonly_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session(url=settings().readonly_dsn):
        yield session
