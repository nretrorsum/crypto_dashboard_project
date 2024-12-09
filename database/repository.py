from typing import List, Any
import uuid

from sqlalchemy import select, insert, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from database.database_connection import async_session, db_dependency
from database.CRUD_class import Database
from database.database_models import UserTable, RefreshToken


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

    async def delete_portfolio(self, user_id, portfolio_id, portfolio_model):
        async with self.db as session:
            stmt = delete(portfolio_model).where(portfolio_model.user_id == user_id).where(portfolio_model.id == portfolio_id)
            await session.execute(stmt)
            await session.commit()

            return {'status': 'portfolio deleted'}

    async def add_help_message(self, user_id, help_model, request):
        async with self.db as session:
            stmt = insert(help_model).values(id = uuid.uuid4(), user_id = user_id, **request.dict())

            await session.execute(stmt)
            await session.commit()

            return {'status': 'Help message added'}

    async def add_refresh_token(self, token, user_email):
        async with self.db as session:
            stmt = insert(RefreshToken).values(id = uuid.uuid4(), token = token).returning(RefreshToken.id)
            result = await session.execute(stmt)
            refresh_token_id = result.scalar()

            id_stmt = update(UserTable).where(UserTable.email == user_email).values(refresh_token=refresh_token_id)
            await session.execute(id_stmt)
            await session.commit()

    async def get_refresh_token(self, user_email):
        async with self.db as session:
            query = select(UserTable).where(UserTable.email == user_email)
            result = await session.execute(query)
            returning_data = result.scalars().first()

            refresh_token_id = returning_data.refresh_token

            query_rt = select(RefreshToken).where(RefreshToken.id == refresh_token_id)
            result = await session.execute(query_rt)
            requested_data = result.scalars().first()
            if not requested_data:
                return None
            data = requested_data
            token_id =  data.id
            return token_id

repository = DatabaseRepository(db_dependency)