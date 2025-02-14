from database.models import PairORM
from database.repository.base import BaseRepository

__all__ = ["PairRepository"]


class PairRepository(BaseRepository):
    model = PairORM
