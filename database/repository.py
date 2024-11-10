from typing import List, AnyStr, Any

from sqlalchemy import select, insert, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from database.database_connection import async_session, db_dependency
from database.CRUD_class import Database

class DatabaseRepository(Database):
    def __init__(self, db):
        self.db = async_session()

    async def get_user(self, id, user_model):
        async with self.db as session:
            query = (
                select(user_model)
                .options(selectinload(user_model.sub))  # Завантаження підписки
                .where(user_model.id == id)
            )
            result = await session.execute(query)
            user = result.scalars().first()
            user_data = user
            user_dict = {
                "id": user_data.id,
                "name": user_data.name,
                "email": user_data.email,
                "subscription": {
                    "id": user_data.sub.id,
                    "tag": user_data.sub.tag,
                    "price": user_data.sub.price,
                },
                "start_time": user_data.start_time,
                "end_time": user_data.end_time,
                "join_date": user_data.join_date,
                "is_active": user_data.is_active,
                "is_verified": user_data.is_verified,
            }
            return user_dict

    async def get_portfolio(self, current_user_id, portfolio_model):
        async with self.db as session:
            query = (
                select(portfolio_model)
                .where(portfolio_model.user_id == current_user_id)
            )

            result = await session.execute(query)
            portfolio = result.scalars().all()

            return portfolio

    async def get_portfolio_by_user(self, user_id, portfolio_id, portfolio_model) -> List[Any]:
        async with self.db as session:
            query = (select(portfolio_model).where(portfolio_model.user_id == user_id).where(portfolio_model.id == portfolio_id))

            result = await session.execute(query)
            data = result.scalars().first()

            return data


    async def add_portfolio(self, user_id, portfolio_model, request):
        async with self.db as session:
            stmt = insert(portfolio_model).values(user_id = user_id, **request.dict())

            await session.execute(stmt)
            await session.commit()

            return {'status': 'success'}

    async def update_portfolio(self, user_id, portfolio_id, portfolio_model, request):
        async with self.db as session:
            stmt = update(portfolio_model).where(portfolio_model.user_id == user_id).where(portfolio_model.id == portfolio_id).values(**request.dict())

            await session.execute(stmt)
            await session.commit()

            return {'status': 'success', 'response': 'Value updated'}

repository = DatabaseRepository(db_dependency)