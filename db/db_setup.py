from typing import Optional, Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from settings.settings import Config

__factory: Optional[Callable[[], Session]] = None
__async_engine: Optional[AsyncEngine] = None
engine: Optional[Engine] = None


def global_init(config: Config):
    global __factory, __async_engine, engine

    if __factory:
        return

    engine = create_engine(config.db.conn_string, echo=False)
    __async_engine = create_async_engine(config.db.async_conn_string, echo=False, poolclass=NullPool)
    __factory = orm.sessionmaker(bind=engine)

    import db.__all_models


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global_init() before using this method.")

    session: Session = __factory()
    session.expire_on_commit = False
    return session


def create_async_session() -> AsyncSession:
    global __async_engine

    if not __async_engine:
        raise Exception("You must call global_init() before using this method.")

    session: AsyncSession = AsyncSession(__async_engine)
    session.sync_session.expire_on_commit = False
    return session


if __name__ == '__main__':
    global_init()
