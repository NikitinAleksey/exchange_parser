from database.models import BalanceORM
from database.repository.base import BaseRepository

__all__ = ["BalanceRepository"]


class BalanceRepository(BaseRepository):
    model = BalanceORM
