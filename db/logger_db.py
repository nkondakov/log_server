import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, func, BIGINT, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.db_configuration import SqlAlchemyBase
from db.models_management import ModelAdmin
from settings.settings import load_config


config = load_config('.env')


class Source(SqlAlchemyBase, ModelAdmin):
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


class Level(SqlAlchemyBase, ModelAdmin):
    __tablename__ = 'level'
    __table_args__ = {"schema": "public"}

    id: uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String, unique=True)
    log = relationship('Log', back_populates='level')


class Log(SqlAlchemyBase, ModelAdmin):
    __tablename__ = 'log'
    __table_args__ = {"schema": "public"}

    id: int = Column(BIGINT, primary_key=True)
    source_id: uuid = Column(UUID(as_uuid=True), ForeignKey('public.source.id'), nullable=True)
    source: Source = relationship('Source', back_populates='log')
    level_id: uuid = Column(UUID(as_uuid=True), ForeignKey('public.level.id'), nullable=True)
    level: Level = relationship('Level', back_populates='log')
    created_at: datetime = Column(DateTime, nullable=False, server_default=func.now(tz=config.misc.time_zone))
