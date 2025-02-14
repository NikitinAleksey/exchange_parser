from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint, VARCHAR
from sqlalchemy.orm import relationship

from database.models.base import BaseORM

__all__ = ["CurrencyORM"]


class CurrencyORM(BaseORM):
    """
    Модель хранения названий криптовалют.
    В дальнейшем могут добавиться другие необходимые поля.

    :param id: Int - уникальный идентификатор записи.
    :param name: Str - Название криптовалюты (пример `BTC` или `USDT`).
    :param exchange_id: Int - идентификатор биржи из таблицы `exchanges`.
    """

    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(20), nullable=False)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False)

    exchange = relationship("Exchange")

    __table_args__ = (UniqueConstraint("name", "exchange_id", name="uix_name_exchange"),)
