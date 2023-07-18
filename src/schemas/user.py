from typing import Literal
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):  # explicitly
    email: EmailStr
    password: str


class UserCreate(BaseModel):  # explicitly
    username: str
    email: EmailStr
    password: str
    repeat_password: str

    oauth: Literal['vlad', 'google', 'github']
    account_id: str


class UserRead(BaseModel):
    username: str
    email: EmailStr

    oauth: Literal['vlad', 'google', 'github']
    account_id: str

    is_active: bool = True
    is_superuser: bool = False

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
