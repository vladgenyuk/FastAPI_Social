from sqlalchemy.ext.asyncio.session import AsyncSession

from src.crud.base_crud import CrudBase, select
from src.models.article import Article


class CrudArticle(CrudBase):

    async def get_my_articles(
            self,
            session: AsyncSession,
            email: str
    ):
        stmt = select(self.model).where(self.model.author_email == email)
        result = await session.execute(stmt)
        result = [dict(r._mapping)['Article'] for r in result]
        return result

    def update_article(
            self,
            session: AsyncSession,
            current_article,
            new_article
    ):
        result = super().update(
            session,
            obj_current=current_article,
            obj_new=new_article
        )
        return result

    def delete_article(
            self,
            session: AsyncSession,
            id: int
    ):
        result = super().delete(
            session,
            id=id
        )
        return result


article = CrudArticle(Article)
