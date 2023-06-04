from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    username: str
    email: str
    expiry_date: Optional[datetime]


class UserInDB(User):
    hashed_password: str
