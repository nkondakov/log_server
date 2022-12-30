from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from db.db_setup import create_async_session


class ModelAdmin:
    @classmethod
    async def create(cls, kwargs: dict) -> None:
        async with create_async_session() as session:
            stmt = insert(cls).values(**kwargs).on_conflict_do_nothing()
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get(cls, kwargs: dict):

        async with create_async_session() as session:
            params = [getattr(cls, key).__eq__(value) for key, value in kwargs.items()]
            query = select(cls).where(*params)
            results = await session.execute(query)
            results = results.scalar()
            return results

    @classmethod
    async def get_or_create(cls, kwargs: dict):
        instance = await cls.get(kwargs)
        if instance:
            return instance
        else:
            await cls.create(kwargs)
            instance = await cls.get(kwargs)
            return instance
