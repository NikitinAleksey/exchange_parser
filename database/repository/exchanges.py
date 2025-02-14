from database.models import ExchangeORM
from database.repository.base import BaseRepository

__all__ = ["ExchangeRepository"]


class ExchangeRepository(BaseRepository):
    model = ExchangeORM
