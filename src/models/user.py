from datetime import date

from typing import Literal
from sqlalchemy import (Boolean, Column, Integer,
                        String, DateTime, func)

from src.db.database import Base, metadata


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=True, unique=True)
    username: str = Column(String, nullable=False)
    registered_at: date = Column(DateTime, default=func.now())
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)

    oauth: Literal['vlad', 'google', 'github'] = Column(String(10), default='vlad')
    account_id: int = Column(String, default=0)
