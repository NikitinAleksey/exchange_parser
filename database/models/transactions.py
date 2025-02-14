from sqlalchemy import Column, Integer, TIMESTAMP, func, UniqueConstraint, Enum, DECIMAL, ForeignKey, CheckConstraint

from database.models.base import BaseORM

__all__ = ["SaleORM", "PurchaseORM", "TransactionORM"]


class BaseTransaction(BaseORM):
    """
    Базовая модель для покупок и продаж.
    Покупка или продажа всегда измеряется в USDT,
    то есть USDT - базовая для всех других валют,
    от нее отталкиваемся.

    :param id: Int - уникальный идентификатор записи.
    :param currency_id: Int - идентификатор валюты в таблице `currencies`.
    :param amount: DECIMAL - Количество купленной/проданной монеты.
    :param price: DECIMAL - Цена покупки/продажи.
    :param exchange_id: Int - идентификатор биржи из таблицы `exchanges`.
    :param created_at: TIMESTAMP - время создания записи.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    amount = Column(DECIMAL(18, 8), nullable=False)
    price = Column(DECIMAL(18, 8), nullable=False)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


class SaleORM(BaseTransaction):
    """
    Таблица продаж. Наследует от BaseTransaction.
    """
    __tablename__ = "sales"


class PurchaseORM(BaseTransaction):
    """
    Таблица покупок. Наследует от BaseTransaction.
    """
    __tablename__ = "purchases"


class TransactionORM(BaseORM):
    """
    Таблица всех транзакций. Хранит данные о всех транзакциях.
    Обязательно нужно указывать ID либо продажи, либо покупки.

    :param id: Int - уникальный идентификатор записи.
    :param type: Str - Тип транзакции (продажа или покупка).
    :param sale_id: Int - ID записи из таблицы `sales`. Будет пустым,
    если type == `purchase`.
    :param purchase_id: Int - ID записи из таблицы `purchases`. Будет пустым,
    если type == `sale`.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(Enum("purchase", "sale"), nullable=False)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    purchase_id = Column(Integer, ForeignKey("purchases.id"))

    __table_args__ = (
        CheckConstraint(
            "(sale_id IS NOT NULL AND purchase_id IS NULL) OR (sale_id IS NULL AND purchase_id IS NOT NULL)",
            name="check_one_id_not_null"
        ),
    )
