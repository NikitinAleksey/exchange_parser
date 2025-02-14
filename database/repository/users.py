from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserORM
from database.repository.base import BaseRepository

__all__ = ["UserRepository"]


class UserRepository(BaseRepository):
    model = UserORM

    async def get_all_users(self, session: AsyncSession):
        stmt = select(self.model.tg_id)
        result = await session.execute(stmt)
        return result.scalars().all()
