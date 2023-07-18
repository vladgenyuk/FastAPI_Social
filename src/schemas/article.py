from datetime import date

from pydantic import BaseModel


class ArticleView(BaseModel):
    id: int
    title: str
    content: str
    author_email: str
    created_at: date
    likes: int
    dislikes: int
    views: int


class ArticleCreate(BaseModel):
    title: str
    content: str
    author_email: str


class ArticleUpdate(ArticleCreate):
    id: int
