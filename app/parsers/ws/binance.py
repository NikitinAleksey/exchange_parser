import json
from typing import List

import aiohttp

from app import AppLogger
from app.parsers.ws.base import BaseWSClient

__all__ = ["BinanceWSClient"]


class BinanceWSClient(BaseWSClient):
    def __init__(self, symbols: List[str], logger: type[AppLogger], url: str):
        super().__init__(symbols=symbols, logger=logger)
        self._set_url(base_url=url)

    async def listen(self, session: aiohttp.ClientSession):
        async with session.ws_connect(url=self.url) as websocket:
            async for msg in websocket:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self.handle_msg(msg=msg)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    await self.handle_error(error=msg)

    def _set_url(self, base_url: str):
        self.url = base_url + '/'.join(self.symbols)

    async def handle_msg(self, msg: aiohttp.WSMsgType.TEXT):
        # TODO реализовать обработку сообзений. НУЖНЫ ТОЛЬКО ПАРАМЕТРЫ ИЗ СПИСКА НИЖЕ
        """
        Пара валют ("s").
        Текущая цена ("c").
        Процентное изменение ("P").
        Объем торгов ("v").
        Время последнего обновления ("E").
        :param msg:
        :return:
        """
        data_dict = json.loads(msg.data)
        ticker_data = data_dict["data"]


    async def handle_error(self, error: aiohttp.WSMsgType.ERROR):
        print(error)



