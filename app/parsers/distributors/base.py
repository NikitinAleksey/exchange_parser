import asyncio
import logging
from abc import ABC, abstractmethod

import aiohttp


__all__ = ["BaseDistributor"]


class BaseDistributor(ABC):
    """
    Базовый класс для дистрибьюторов.
    ВАЖНО!: Каждый наследник должен называться по схеме:
    название биржи + Distributor. Иначе он не будет внесен в список
    в функции matching в app.utils.utils, и не будет работать совсем.
    """
    def __init__(self, ws_url: str, symbols: str, logger=None):
        self.symbols = self._format_symbols(symbols=symbols)
        self.ws_url = ws_url
        self.ws_symbols = set()
        self.api_symbols = set()
        self.logger = logger
        self.log = (logger(type(self).__name__)
                    if logger
                    else logging.getLogger(type(self).__name__))

    async def distribute_symbols(self):
        """Проверяет доступность символов через WebSocket и обновляет множества. Использует _check_symbol_via_ws
        для проверки. После нее запускает сервисы своей биржи."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for symbol in self.symbols:
                tasks.append(self._check_symbol(symbol=symbol, session=session))

            results = await asyncio.gather(*tasks)

            for symbol, result in zip(self.symbols, results):
                if result:
                    self.ws_symbols.add(symbol)
                else:
                    self.api_symbols.add(symbol.split('@')[0].upper())

        await self._run_services()

    @staticmethod
    def _format_symbols(symbols: str):
        return [f"{symbol.lower()}@ticker" for symbol in symbols.split(',')]

    @abstractmethod
    async def _run_services(self):
        """Запускает сервисы ws и api для своей биржи."""

    @abstractmethod
    async def _check_symbol(self, symbol: str, session: aiohttp.ClientSession) -> bool:
        """Проверяет доступность конкретного символа для WebSocket.
        Должен быть реализован в наследуемых классах. Должен вернуть True/False"""

    @abstractmethod
    async def _run_ws_service(self, ws_symbols: set):
        """Запускает сервис WebSocket для доступных символов.
        Общая логика для обработки WebSocket соединений."""

    @abstractmethod
    async def _run_api_service(self, api_symbols: set):
        """Запускает сервис API для недоступных символов.
        Общая логика для обработки API запросов."""
