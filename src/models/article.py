from datetime import date

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey

from src.db.database import metadata, Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title: str = Column(String(length=100))
    content: str = Column(String)
    created_at: date = Column(DateTime, default=func.now())
    author_email: int = Column(String, ForeignKey('users.email'))
