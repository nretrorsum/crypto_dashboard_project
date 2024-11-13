from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from auth.auth import get_current_user
from database.database_models import UserTable, UserPortfolio
from routers.cache_operations import get_cached_user, cache_user
from routers.schemas import ReadUser, AddPortfolio, ReadPortfolio, UpdateUserPortfolio
from database.repository import repository
from app_functions.investment import investment
from auth.auth import user_dependency

user_router = APIRouter()
@user_router.get('/user/{id}', response_model=ReadUser)
async def read_user(auth: user_dependency, id: int) -> ReadUser:
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    cached_user = get_cached_user(id)
    if cached_user:
        return cached_user

    data = await repository.get_user(id, UserTable)
    if data:
        user_data = ReadUser.from_orm(data)
        cache = cache_user(id, user_data)
        return user_data


@user_router.get('/portfolio/{id}')
async def read_user_portfolio(id: int, auth: user_dependency) -> List[ReadPortfolio]:
    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    data = await repository.get_portfolio(id, UserPortfolio)
    if len(data) == 0:
        raise HTTPException(status_code=404, detail="No portfolio found for this user")

    return data
@user_router.post('/user/{id}/portfolio', status_code= status.HTTP_201_CREATED)
async def add_user_portfolio(auth: user_dependency, id: int, request: AddPortfolio):
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    data_insert = await (
        repository
        .add_portfolio(user_id = id, portfolio_model = UserPortfolio, request = request)
    )
    return data_insert

@user_router.patch('/user/{id}/portfolio/{portfolio_id}', status_code=status.HTTP_200_OK)
async def update_user_portfolio(auth: user_dependency, id: int, portfolio_id: int, request: UpdateUserPortfolio):
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    data_update = await repository.update_portfolio(user_id = id, portfolio_id = portfolio_id, portfolio_model= UserPortfolio, request = request)

    return data_update

@user_router.delete('/user/{id}/portfolio/{portfolio_id}')
async def delete_user_portfolio(auth: user_dependency, id: int, portfolio_id: int):
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if auth['user_id'] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    data_delete = await repository.delete_portfolio(user_id = id, portfolio_id = portfolio_id, portfolio_model= UserPortfolio)

    return data_delete

@user_router.get('/get_profit/{user_id}/{portfolio_id}', status_code=200)
async def get_profit(user_id: int, portfolio_id: int):
    performance_data = await investment.calculate_portfolio_performance(user_id, portfolio_id)
    return {"status": "success", "data": performance_data}
