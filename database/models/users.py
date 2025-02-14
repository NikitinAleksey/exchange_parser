from sqlalchemy import Column, Integer, Boolean

from database.models import BaseORM

__all__ = ["UserORM"]


class UserORM(BaseORM):
    """
    Модель хранения списка пользователей, которым доступен бот.

    :param id: Int - уникальный идентификатор записи.
    :param tg_id: Int - id пользователя в телеграм.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False)
    is_admin = Column(Boolean)
