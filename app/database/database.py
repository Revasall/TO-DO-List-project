from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator

from app.config import config
from app.database.models import Base
from contextlib import asynccontextmanager


#---Create engine and session---
engine = create_async_engine(config.DATABASE_URL, echo=config.ECHO_SQL)
async_session = async_sessionmaker(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:       
        await conn.run_sync(Base.metadata.create_all)
    yield 
    await engine.dispose()

