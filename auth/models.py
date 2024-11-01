from datetime import datetime
from typing import List, Optional
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
