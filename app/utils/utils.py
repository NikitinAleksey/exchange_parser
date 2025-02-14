from pydantic_settings import BaseSettings

from app.parsers.distributors.base import BaseDistributor

__all__ = [
    "check_symbol",
    "matching"
]


def check_symbol(symbol: str) -> bool:
    """
    Проверят, начинается ли пара с BTC.

    :param symbol: Пара символов.
    :return: Bool.
    """
    return symbol.startswith('BTC')


def matching(
        distributors: list[type[BaseDistributor]],
        settings: list[type[BaseSettings]]
) -> list[tuple[type[BaseDistributor], type[BaseSettings]]]:
    """
    Сопоставляет дистрибьюторы бирж с конфигами бирж.
    ВАЖНО!:
    Названия классов дистрибьюторов по схеме: название биржи + Distributor
    Названия классов конфигов по схеме: название биржи + Settings

    :param settings: Список конфигов для бирж.
    :param distributors: Список дистрибьюторов для бирж.
    :return: Список кортежей, где первый элемент - дистрибьютор,
    а второй - соответствующий конфиг.
    """
    matches = []
    for distributor in distributors:
        distributor_name = distributor.__name__.lower()
        exchange_name = distributor_name.rstrip("distributor")
        for setting in settings:
            setting_name = setting.__name__.lower()
            if setting_name.startswith(exchange_name):
                matches.append((distributor, setting))
                break

    return matches
