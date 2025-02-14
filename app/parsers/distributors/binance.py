import asyncio

import aiohttp

from app.parsers.distributors.base import BaseDistributor
from app.parsers.ws.binance import BinanceWSClient
from app.parsers.api import BinanceAPIClient

__all__ = ["BinanceDistributor"]


class BinanceDistributor(BaseDistributor):
    def __init__(
        self,
        ws_url: str,
        symbols: str,
        api_url: str,
        api_interval: int,
        ws_streams_url: str,
        logger=None
    ):
        super().__init__(ws_url, symbols, logger)
        self.api_url = api_url
        self.api_interval = int(api_interval)
        self.ws_streams_url = ws_streams_url

    async def _check_symbol(self, symbol: str, session: aiohttp.ClientSession) -> bool:
        """Подключается к ws своей биржи, и если получает сообщение, не являющееся ошибкой, то возвращает True.
        Если получит ошибку или ответа нет в течение 10 секунд, вернет False."""
        self.log.debug("Проверка доступности символов в веб-сокетах Binance.")

        try:
            async with session.ws_connect(self.ws_url + symbol) as websocket:
                msg = await asyncio.wait_for(websocket.receive(), timeout=10)

                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()
                    if "error" not in data:
                        self.log.debug(f'По символу {symbol} есть ответ. Добавляем в ws_symbols')
                        return True

        except (asyncio.TimeoutError, aiohttp.ClientError) as exc:
            self.log.debug(f'По символу {symbol} нет ответа, или возникла ошибка. Добавляем в api_symbols')

        return False

    async def _run_services(self):
        self.log.debug("Запускаем сервисы веб-сокетов и АПИ.")

        await asyncio.gather(
            self._run_ws_service(self.ws_symbols),
            self._run_api_service(self.api_symbols)
        )

    async def _run_ws_service(self, ws_symbols: set):
        self.log.debug("Запускаем веб-сокет.")

        binance_ws_client = BinanceWSClient(
            symbols=list(ws_symbols),
            url=self.ws_streams_url,
            logger=self.logger
        )
        async with binance_ws_client as session:
            await binance_ws_client.listen(session=session)

    async def _run_api_service(self, api_symbols: set):
        self.log.debug("Запускаем АПИ.")

        binance_api_client = BinanceAPIClient(
            symbols=list(api_symbols),
            base_url=self.api_url,
            interval=self.api_interval
        )
        async with binance_api_client as session:
            await binance_api_client.start_scheduler(session=session)
