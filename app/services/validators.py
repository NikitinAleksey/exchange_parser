from datetime import datetime
from typing import Optional, ClassVar

from pydantic import BaseModel, ConfigDict, condecimal, Field, field_validator, constr

__all__ = [
    "PairsValidator",
    "SalePurchaseValidator",
    "TransactionValidator",
    "CurrencyValidator",
    "ExchangeValidator"
]


class BaseValidator(BaseModel):
    id: Optional[int] = Field(default=None, exclude=True)

    config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class PairsValidator(BaseValidator):
    base_currency_id: int
    quote_currency_id: int
    price: condecimal(max_digits=18, decimal_places=8)
    volume: condecimal(max_digits=18, decimal_places=8)
    price_change_percent: condecimal(max_digits=18, decimal_places=8)
    exchange_id: int
    updated_at: datetime


class SalePurchaseValidator(BaseValidator):
    currency_id: int
    amount: condecimal(max_digits=18, decimal_places=8)
    price: condecimal(max_digits=18, decimal_places=8)
    exchange_id: int
    created_at: datetime


class TransactionValidator(BaseValidator):
    type: str
    sale_id: int
    purchase_id: int

    @field_validator("type")
    def validate_type(cls, value: str):
        """
        Проверяет, что тип является покупкой или продажей.

        :param value: Str - тип транзакции, которую нужно проверить.
        :return: Str - валидированный тип транзакции.
        """
        value = value.lower()
        if value not in ["purchase", "sale"]:
            raise ValueError(
                "Тип транзакции может быть только `purchase` или `sale`."
            )
        return value


class CurrencyValidator(BaseValidator):
    name: constr(min_length=2, max_length=20)
    exchange_id: int

    @field_validator("name")
    def upper_case(cls, value: str):
        """Вернет валюту в верхнем регистре."""
        return value.upper()


class ExchangeValidator(BaseValidator):
    name: constr(min_length=3, max_length=50)
    api_token: constr(min_length=3, max_length=255)
    updated_at: datetime
