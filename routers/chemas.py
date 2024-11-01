from pydantic import BaseModel
from datetime import datetime

class ReadUser(BaseModel):
    id:int
    name:str
    email:str
    subscription: int
    start_time: datetime
    end_time: datetime
    join_date: datetime
    is_active: bool
    is_verified: bool