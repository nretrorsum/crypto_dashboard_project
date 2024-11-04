from typing import List

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class Subscription(BaseModel):
    id: int
    tag: str
    price: int

class ReadUser(BaseModel):
    id:int
    name:str
    email:str
    subscription: Subscription
    start_time: datetime
    end_time: datetime
    join_date: datetime
    is_active: bool
    is_verified: bool

class AddPortfolio(BaseModel):
    id: int
    user_id: int
    ticker: str
    value: int
    price: Decimal
    setup_time: datetime

class ReadPortfolio(BaseModel):
    id: int
    user_id: int
    ticker: str
    value: int
    price: Decimal
    setup_time: datetime