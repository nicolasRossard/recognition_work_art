from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserUpdate(BaseModel):
    password: str


class UserDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    password: str
