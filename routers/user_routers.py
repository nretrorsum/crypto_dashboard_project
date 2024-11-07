from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from datetime import datetime

from sqlalchemy.orm import selectinload
from starlette import status
from auth.auth import get_current_user
from database.database_connection import db_dependency
from database.database_models import UserTable, UserPortfolio, Subscription
from routers.schemas import ReadUser, AddPortfolio, ReadPortfolio
from database.repository import DatabaseRepository

repository = DatabaseRepository(db_dependency)
user_router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


@user_router.get('/user/{id}', response_model=ReadUser)
async def read_user(auth: user_dependency, id: int) -> ReadUser:
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    data = await repository.get_user(id, UserTable)
    return data

@user_router.post('/user/{id}/portfolio', status_code= status.HTTP_201_CREATED)
async def add_user_portfolio(auth: user_dependency, id: int, db:db_dependency, request: AddPortfolio):
    pass
@user_router.get('/user/{id}/portfolio', response_model=List[ReadPortfolio])
async def get_user_portfolio(auth:user_dependency, id: int, db:db_dependency):
    pass

