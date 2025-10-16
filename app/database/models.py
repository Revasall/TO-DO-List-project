from typing import List
from sqlalchemy import (
    Boolean,
    String,
    Integer,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import config
from datetime import datetime




#---Create engine and session---
engine = create_async_engine(config.DATABASE_URL, echo=config.ECHO_SQL)
async_session = async_sessionmaker(engine)

# ---Base---
class Base(DeclarativeBase):
    # A common base for all models
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

# ---Model Task---
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str|None] = mapped_column(String, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime|None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))



async def async_models_main():
    async with engine.begin() as conn:        
        await conn.run_sync(Base.metadata.create_all)
