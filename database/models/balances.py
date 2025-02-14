from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship

from database.models.base import BaseORM

__all__ = ["BalanceORM"]


class BalanceORM(BaseORM):
    """
    Модель хранения текущего баланса монет на кошельках.

    :param id: Int - уникальный идентификатор записи.
    :param currency_id: Int - идентификатор валюты в таблице `currencies`.
    :param amount: DECIMAL - Сумма валюты на балансе.
    :param exchange_id: Int - идентификатор биржи из таблицы `exchanges`.
    :param updated_at: TIMESTAMP - время обновления записи.
    """

    __tablename__ = "balances"

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    amount = Column(DECIMAL(18, 8), nullable=False)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    currency = relationship("Currency")
    exchange = relationship("Exchange")

    __table_args__ = (UniqueConstraint("currency_id", "exchange_id", name="uix_currency_exchange"),)
