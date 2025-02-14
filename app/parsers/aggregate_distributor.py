import asyncio
import logging

from pydantic_settings import BaseSettings

from app.parsers import distributors
from app.utils import matching

__all__ = ["DistributorAggregator"]


class DistributorAggregator:
    """
    Собирает все существующие дистрибьюторы и запускает их.
    Любой новый дистрибьютор должен быть добавлен в app.parsers.__init__.
    """

    def __init__(
            self,
            symbols: str,
            settings_list: list[type[BaseSettings]],
            logger=None
    ):
        self.log = (logger(type(self).__name__)
                    if logger
                    else logging.getLogger(type(self).__name__))
        self.log.debug("Инициализируем Дистриьтбтор Аггрегатор!!!!!!!!")
        self.symbols = symbols
        self.pairs_list = self.comparison(
            distributors_list=distributors,
            settings_list=settings_list
        )
        self.logger = logger

    async def launch(self) -> None:
        """Запуск всех дистрибьюторов."""
        self.log.debug("Запускаем все дистрибьюторы.")
        tasks = []

        for distributor, config in self.pairs_list:
            config_instance = config()
            curr_distributor = distributor(
                symbols=self.symbols,
                ws_url=config_instance.WS_URL,
                api_url=config_instance.API_URL,
                api_interval=config_instance.INTERVAL,
                ws_streams_url=config_instance.WS_STREAMS_URL,
                logger=self.logger
            )
            tasks.append(curr_distributor.distribute_symbols())

        await asyncio.gather(*tasks)

    def comparison(self, distributors_list, settings_list):
        """
        Запускает функцию сопоставления. В результате будет список кортежей
        для корректного запуска. Подробнее - в документации matching.
        """
        self.log.debug("Запускаем сопоставление дистрибьюторов с конфигами.")

        return matching(
            distributors=distributors_list,
            settings=settings_list
        )
