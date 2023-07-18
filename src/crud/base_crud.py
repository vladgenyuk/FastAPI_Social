from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, func, update


class CrudBase:
    def __init__(self, model):
        self.model = model

    async def get_paginated(
            self,
            session: AsyncSession,
            page: int = 1,
            page_size: int = 2
    ):
        offset = (page - 1) * page_size
        stmt = select(self.model).offset(offset).limit(page_size)
        result = await session.execute(stmt)
        result = [dict(r._mapping)['Article'] for r in result]
        return result

    async def get_count(
            self,
            session: AsyncSession
    ) -> int:
        stmt = select(func.count()).select_from(self.model)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
            self,
            session: AsyncSession,
            create_obj
    ):
        validated_data = jsonable_encoder(create_obj)
        stmt = insert(self.model).values(**validated_data)
        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(e)
            )
        return validated_data

    async def update(
            self,
            session: AsyncSession,
            obj_current,
            obj_new
    ):
        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )

        obj_data = jsonable_encoder(obj_new)
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])

        stmt = update(self.model).values(**update_data).where(self.model.id == obj_current.id)

        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(e)
            )
        return obj_current

    async def delete(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)

        response = await session.execute(stmt)
        obj = response.scalar_one()
        await session.delete(obj)
        await session.commit()
        return obj
