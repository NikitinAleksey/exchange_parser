"""
Table pairs {
  updated_at timestamp
}
"""
from sqlalchemy import Column, Integer, TIMESTAMP, func, UniqueConstraint, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from database.models.base import BaseORM

__all__ = ["PairORM"]


class PairORM(BaseORM):
    """
    Модель пар в таблице 'pairs'. Содержит основные данные,
    которые я получаю из веб-сокетов и/или API.

    :param id: Int - уникальный идентификатор записи.
    :param base_currency_id: Int - ID основной валюты из таблицы `currencies`.
        Вместе с quote_currency_id образуют торговую пару.
    :param quote_currency_id: Int - ID валюты котировки из таблицы `currencies`.
        Вместе с base_currency_id образуют торговую пару.
    :param price: DECIMAL - Цена основной валюты за валюту котировки.
    :param volume: DECIMAL - Объем торгов.
    :param price_change_percent: DECIMAL - Процентное изменение.
    :param exchange_id: Int - идентификатор биржи из таблицы `exchanges`.
    :param updated_at: TIMESTAMP - время обновления записи.
    """

    __tablename__ = "pairs"

    id = Column(Integer, primary_key=True)
    base_currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    quote_currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    price = Column(DECIMAL(18, 8), nullable=False)
    volume = Column(DECIMAL(18, 8), nullable=False)
    price_change_percent = Column(DECIMAL(5, 2), nullable=False)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    base_currency = relationship("Currency")
    quote_currency = relationship("Currency")
    exchange = relationship("Exchange")

    __table_args__ = (UniqueConstraint(
        "base_currency_id",
        "quote_currency_id",
        "exchange_id",
        name="uix_currencies_exchange"
            ),
        )
