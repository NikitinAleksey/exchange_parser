from abc import ABC, abstractmethod
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp

__all__ = ["BaseAPIClient"]


class BaseAPIClient(ABC):
    def __init__(self, symbols: List[str], base_url: str, interval: int):
        self.symbols = symbols
        self._set_url(base_url=base_url)
        self.connection = None
        self.interval = interval

    @abstractmethod
    def _set_url(self, base_url: str):
        ...

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def start_scheduler(self, session: aiohttp.ClientSession):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.api_request, 'interval', seconds=self.interval, kwargs={"session": session})

    @abstractmethod
    async def api_request(self, session: aiohttp.ClientSession):
        ...

    @abstractmethod
    async def handle_msg(self, msg: aiohttp.WSMsgType.TEXT):
        ...

    @abstractmethod
    async def handle_error(self, error: aiohttp.WSMsgType.ERROR):
        ...
