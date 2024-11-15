import uuid
from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel
import uuid

class Subscription(BaseModel):
    id:int
    tag: str
    price: int

class User(BaseModel):
    id: uuid.UUID
    name:str
    email:str
    hashed_password:str
    subscription: int
    start_time: datetime
    end_time: datetime
    join_date: datetime
    is_active: bool
    is_verified: bool

class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'
    user_id: uuid.UUID

class UserPortfolio(BaseModel):
    id: int
    user_id: uuid.UUID
    ticker: str
    value: Decimal
    price: Decimal
    setup_time: datetime

