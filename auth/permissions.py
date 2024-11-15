from typing import Annotated
from fastapi import Depends
from database.database_models import UserTable
from database.repository import repository
from uuid import UUID


async def check_permissions(id: UUID):
    user_data = await repository.get_user(id, UserTable)
    if user_data['subscription']['id'] != 2:
        return False
    else: return True

permission_dependency = Annotated[bool, Depends(check_permissions)]