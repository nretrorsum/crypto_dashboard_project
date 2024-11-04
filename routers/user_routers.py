from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from datetime import datetime

from sqlalchemy.orm import selectinload
from starlette import status

from auth.auth import db_dependency, get_current_user
from database.database_models import UserTable, UserPortfolio
from routers.schemas import ReadUser, AddPortfolio, ReadPortfolio

user_router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


@user_router.get('/user/{id}', response_model=ReadUser)
async def read_user(auth: user_dependency, id: int, db: db_dependency):
    if auth is None or auth['user_id'] != id:
        raise HTTPException(status_code=403, detail='Not authenticated')

    query = (
        select(UserTable)
        .options(selectinload(UserTable.sub))  # Завантаження підписки
        .where(UserTable.id == id)
    )

    result = await db.execute(query)
    user_data = result.scalars().first()

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Повертаємо користувача з `sub` як `subscription`
    return {
        "id": user_data.id,
        "name": user_data.name,
        "email": user_data.email,
        "subscription": {
            "id": user_data.sub.id,
            "tag": user_data.sub.tag,
            "price": user_data.sub.price
        },
        "start_time": user_data.start_time,
        "end_time": user_data.end_time,
        "join_date": user_data.join_date,
        "is_active": user_data.is_active,
        "is_verified": user_data.is_verified
    }

@user_router.post('/user/{id}/portfolio', status_code= status.HTTP_201_CREATED)
async def add_user_portfolio(auth: user_dependency, id: int, db:db_dependency, request: AddPortfolio):
    if auth is None:
        raise HTTPException(status_code = 403, detail= 'Not authenticated')

    if auth['user_id'] != id:
        raise HTTPException(status_code = 403, detail= 'Not authenticated')

    create_portfolio = UserPortfolio(
        id = request.id,
        user_id = id,
        ticker = request.ticker,
        value = request.value,
        price = request.price,
        setup_time= datetime.utcnow()
    )

    db.add(create_portfolio)
    await db.commit()

    return {'status': 'Portfolio created'}
@user_router.get('/user/{id}/portfolio', response_model=List[ReadPortfolio])
async def get_user_portfolio(auth:user_dependency, id: int, db:db_dependency):
    if auth is None:
        raise HTTPException(status_code = 403, detail= 'Not authenticated')

    if auth['user_id'] != id:
        raise HTTPException(status_code = 403, detail= 'Not authenticated')

    data = await db.execute(
        select(UserPortfolio)
        .where(UserPortfolio.user_id == id)
    )

    result = data.scalars().all()

    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return result