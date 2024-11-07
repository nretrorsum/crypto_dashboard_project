from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session

from config import DB_PASS, DB_HOST, DB_PORT, DB_NAME, DB_USER

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DB_URL)

async_session = async_sessionmaker(bind= engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
            yield session

db_dependency = Annotated[Session, Depends(get_db)]