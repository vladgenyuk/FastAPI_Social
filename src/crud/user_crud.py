import hashlib

from fastapi import HTTPException

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from src.crud.base_crud import CrudBase
from src.models.user import User


class CrudUser(CrudBase):
    async def unique_user(
            self,
            session: AsyncSession,
            data
    ):
        stmt = select(self.model)\
            .filter(self.model.email == data['email'])
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            return False
        return result

    def get_user_by_id(
            self,
            session: AsyncSession,
            id: int
    ):
        result = super().get_by_id(session, id)
        return result

    async def get_registered_user(
            self,
            session: AsyncSession,
            email: str,
            password: str
    ):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        stmt = select(self.model)\
            .where(self.model.email == email)\
            .where(self.model.hashed_password == hashed_password)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    def get_user_count(
            self,
            session: AsyncSession
    ):
        result = super().get_count(session)
        return result

    async def create_user(
            self,
            session: AsyncSession,
            data
    ):
        if not await self.unique_user(session, data):
            raise HTTPException(
                status_code=403,
                detail='User with this email already exists'
            )

        if data['password'] != data['repeat_password']:
            raise HTTPException(
                status_code=401,
                detail='Your repeated password is different'
            )

        data['hashed_password'] = hashlib.sha256(data['password'].encode()).hexdigest()
        data.pop('password'), data.pop('repeat_password')
        result = await super().create(session, data)
        return result

    def update_user(
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

    def delete_user(
            self,
            session: AsyncSession,
            id: int
    ):
        result = super().delete(
            session,
            id=id
        )
        return result


user = CrudUser(User)

