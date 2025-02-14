from sqlalchemy import Column, Integer, TIMESTAMP, func, UniqueConstraint, VARCHAR

from database.models.base import BaseORM

__all__ = ["ExchangeORM"]


class ExchangeORM(BaseORM):
    """
    Модель биржи в таблице 'exchanges'.

    :param id: Int - уникальный идентификатор записи.
    :param name: Str - название биржи.
    :param api_token: Str - Секретный токен для операций на барже (зашифрован).
    :param updated_at: TIMESTAMP - время обновления записи.
    """

    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    api_token = Column(VARCHAR(255), nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("name"),)
