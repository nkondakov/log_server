from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from settings.db import async_session


@async_session
async def create(async_session, cls, kwargs: dict, value: str = None):
    if value:
        stmt = insert(cls).values(**kwargs).returning(getattr(cls, value))
    else:
        stmt = insert(cls).values(**kwargs)

    instance = await async_session.execute(stmt)
    await async_session.commit()
    return instance.scalar()


@async_session
async def get(async_session, cls, kwargs: dict):
    params = [getattr(cls, key).__eq__(value) for key, value in kwargs.items()]
    query = select(cls).where(*params)
    results = await async_session.execute(query)
    return results.scalar()


async def get_or_create(cls, kwargs: dict, value: str = None):
    instance = await get(cls, kwargs)
    if instance:
        return getattr(instance, value)
    else:
        instance = await create(cls, kwargs, value)
        return instance
