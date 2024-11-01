from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from auth.auth import db_dependency
from database.database_models import UserTable
from routers.chemas import ReadUser

user_router = APIRouter()

@user_router.get('/user/{id}', response_model=ReadUser)
async def read_user(id: int, db: db_dependency):
    user = await db.execute(
        select(UserTable).where(UserTable.id == id)
    )
    result = user.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result