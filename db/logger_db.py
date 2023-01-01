import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, func, BIGINT, ForeignKey, SMALLINT, INTEGER, TIMESTAMP, DATETIME
from sqlalchemy.dialects.postgresql import UUID, JSON, json
from sqlalchemy.orm import relationship

from db.db_configuration import SqlAlchemyBase
from settings.settings import load_config


config = load_config('.env')


class Source(SqlAlchemyBase):
    __tablename__ = 'source'
    __table_args__ = {"schema": "public"}

    id: uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String, unique=True)
    log = relationship('Log', back_populates='source')
    token: uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    created_at: datetime = Column(DateTime, nullable=False, server_default=func.now(tz=config.misc.time_zone))
    changed_at: datetime = Column(DateTime,
                                  nullable=False,
                                  server_default=func.now(tz=config.misc.time_zone),
                                  onupdate=func.current_timestamp())


class Level(SqlAlchemyBase):
    __tablename__ = 'level'
    __table_args__ = {"schema": "public"}

    id: int = Column(SMALLINT, primary_key=True)
    name: str = Column(String, unique=True)
    numeric_value: int = Column(SMALLINT, unique=True)
    log = relationship('Log', back_populates='level')


class Log(SqlAlchemyBase):
    __tablename__ = 'log'
    __table_args__ = {"schema": "public"}

    id: int = Column(BIGINT, primary_key=True)
    source_id: uuid = Column(UUID(as_uuid=True), ForeignKey('public.source.id'), nullable=True)
    source: Source = relationship('Source', back_populates='log')
    level_id: int = Column(SMALLINT, ForeignKey('public.level.id'), nullable=False)
    level: Level = relationship('Level', back_populates='log')
    file_path: str = Column(String, nullable=True)
    filename: str = Column(String, nullable=True)
    module: str = Column(String, nullable=True)
    logger_name: str = Column(String, nullable=True)
    function_name: str = Column(String, nullable=True)
    line_of_code: int = Column(INTEGER, nullable=True)
    message: str = Column(String, nullable=True)
    process: str = Column(String, nullable=True)
    process_name: str = Column(String, nullable=True)
    exception_info: str = Column(String, nullable=True)
    exception_text: str = Column(String, nullable=True)
    created_at: datetime = Column(TIMESTAMP, nullable=True)
    received_at: datetime = Column(DateTime, nullable=False, server_default=func.now(tz=config.misc.time_zone))
