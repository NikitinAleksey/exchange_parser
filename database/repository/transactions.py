from database.models import SaleORM, PurchaseORM, TransactionORM
from database.repository.base import BaseRepository

__all__ = [
    "SaleRepository",
    "PurchaseRepository",
    "TransactionRepository"
]


class SaleRepository(BaseRepository):
    model = SaleORM


class PurchaseRepository(BaseRepository):
    model = PurchaseORM


class TransactionRepository(BaseRepository):
    model = TransactionORM
