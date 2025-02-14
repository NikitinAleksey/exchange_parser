from typing import List

import aiohttp

from app.parsers.api.base import BaseAPIClient

__all__ = ["BinanceAPIClient"]


class BinanceAPIClient(BaseAPIClient):

    def __init__(self, symbols: List[str], base_url: str, interval: int):
        super().__init__(symbols, base_url, interval)

    def _set_url(self, base_url: str):
        result = f"""[{",".join(f'"{symbol}"' for symbol in self.symbols)}]"""
        self.url = base_url + result

    async def api_request(self, session: aiohttp.ClientSession):
        pass

    async def handle_msg(self, msg: aiohttp.WSMsgType.TEXT):
        pass

    async def handle_error(self, error: aiohttp.WSMsgType.ERROR):
        pass
