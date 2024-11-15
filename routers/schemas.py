from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
import uuid

class Subscription(BaseModel):
    id: int
    tag: str
    price: int

class ReadUser(BaseModel):
    id:uuid.UUID
    name:str
    email:str
    subscription: Subscription
    start_time: datetime
    end_time: datetime
    join_date: datetime
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

class AddPortfolio(BaseModel):
    ticker: str
    value: Decimal
    price: Decimal
    setup_time: datetime

class ReadPortfolio(BaseModel):
    id: int
    user_id: uuid.UUID
    ticker: str
    value: Decimal
    price: Decimal
    setup_time: datetime

class UpdateUserPortfolio(BaseModel):
    value: Decimal

class AddHelpMessage(BaseModel):
    text: str
    add_time: datetime
