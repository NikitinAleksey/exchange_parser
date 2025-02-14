from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BaseORM

__all__ = ["BaseRepository"]


class BaseRepository(ABC):
    """
    Базовый класс для работы с бд. В наследниках нужно лишь реализовать
    специфические для него методы (или переопределить текущие)
    и указать модель, с которой он должен работать.

    :param model: Base - модель, к которой относятся запросы.
    """
    model: type[BaseORM]

    @staticmethod
    async def create(session: AsyncSession, item: BaseORM):
        """
        Создает новый элемент в базе данных.

        :param session: AsyncSession - асинхронная сессия для работы с базой данных.
        :param item: Base - объект для сохранения в базе данных.
        :return: None.
        """
        session.add(item)
        await session.commit()
        return item

    async def read(self, session: AsyncSession, item_id: int):
        """
        Читает данные из базы данных по tg_id и модели.

        :param item_id: Id записи в таблице.
        :param session: AsyncSession - асинхронная сессия для работы с базой данных.
        :return: Объект модели или None, если данные не найдены.
        """
        stmt = select(self.model).where(self.model.id == item_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def update(session: AsyncSession, item: BaseORM):
        """
        Обновляет данные элемента в базе данных.

        :param session: AsyncSession - асинхронная сессия для работы с базой данных.
        :param item: Base - объект с обновленными данными.
        :return: None.
        """
        merged_item = await session.merge(item)
        await session.commit()
        return merged_item

    @staticmethod
    async def delete(session: AsyncSession, item: BaseORM):
        """
        Удаляет элемент из базы данных.

        :param session: AsyncSession - асинхронная сессия для работы с базой данных.
        :param item: Base - объект, который необходимо удалить.
        :return: None.
        """
        await session.delete(item)
        await session.commit()
        return item
