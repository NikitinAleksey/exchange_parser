from abc import ABC, abstractmethod
from typing import List

import aiohttp

from app import AppLogger
from redis_client.queue.producer import RedisProducer
from redis_client.connector import RedisConnector

__all__ = ["BaseWSClient"]


class BaseWSClient(ABC):
    def __init__(
            self,
            symbols: List[str],
            logger: type[AppLogger]
    ):
        self.symbols = symbols
        self.log = logger(name=type(self).__name__)

    @abstractmethod
    def _set_url(self, base_url: str):
        ...

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def listen(self, session: aiohttp.ClientSession):
        ...

    @abstractmethod
    async def handle_msg(self, msg: aiohttp.WSMsgType.TEXT):
        ...

    @abstractmethod
    async def handle_error(self, error: aiohttp.WSMsgType.ERROR):
        ... # TODO докстринги написать ко всем абстрактным методам


