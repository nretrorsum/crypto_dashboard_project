from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from auth.auth import get_current_user
from database.database_connection import db_dependency
from database.database_models import UserTable, UserPortfolio
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

@user_router.get('/portfolio/{id}')
async def read_user_portfolio(auth: user_dependency, id: int) -> List[ReadPortfolio]:
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    data = await repository.get_portfolio(id, UserPortfolio)
    if len(data) == 0:
        raise HTTPException(status_code=404, detail="Not find such portfolio for this user")

    return data

@user_router.post('/user/{id}/portfolio', status_code= status.HTTP_201_CREATED)
async def add_user_portfolio(auth: user_dependency, id: int, request: AddPortfolio):
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    data_insert = await (
        repository
        .add_portfolio(user_id = id,
                       portfolio_model = UserPortfolio,
                       request = request
                       )
    )
    return data_insert

