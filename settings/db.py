from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from settings.settings import load_config

config = load_config('.env')
async_engine = create_async_engine(config.db.async_conn_string, echo=False, poolclass=NullPool)
AsyncLocalSession = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_async_session():
    session = AsyncLocalSession()
    try:
        yield session
    except Exception as e:
        print(e)
        await session.rollback()
    finally:
        await session.close()


def async_session(func):
    async def wrapper(*args, **kwargs):
        async with get_async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper
