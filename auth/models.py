from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Subscription(BaseModel):
    id:int
    tag: str
    price: int

class User(BaseModel):
    id:int
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
    user_id: int

class UserPortfolio(BaseModel):
    id: int
    user_id: int
    ticker: str
    value: Decimal
    price: Decimal
    setup_time: datetime

class Permission(str, Enum):
    FREE_PLAN = 'free'
    PRO_PLAN = 'pro'
