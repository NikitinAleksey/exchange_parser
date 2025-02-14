from database.repository.balances import BalanceRepository
from database.repository.currencies import CurrencyRepository
from database.repository.exchanges import ExchangeRepository
from database.repository.pairs import PairRepository
from database.repository.transactions import SaleRepository, PurchaseRepository, TransactionRepository
from database.repository.users import UserRepository

__all__ = ["RepositoryAggregator"]


class RepositoryAggregator:
    balance = BalanceRepository
    currency = CurrencyRepository
    exchange = ExchangeRepository
    pair = PairRepository
    sale = SaleRepository
    purchase = PurchaseRepository
    transaction = TransactionRepository
    user = UserRepository
