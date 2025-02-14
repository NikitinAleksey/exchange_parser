from database.models import CurrencyORM
from database.repository.base import BaseRepository

__all__ = ["CurrencyRepository"]


class CurrencyRepository(BaseRepository):
    model = CurrencyORM
