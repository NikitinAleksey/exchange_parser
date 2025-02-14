import asyncio

from app.parsers.aggregate_distributor import DistributorAggregator
from database.pg_connector import PostgresConnector
from database import RepositoryAggregator
from app.controllers import ControllerAggregator
from app.parsers.distributors.base import BaseDistributor
from redis_client import RedisConnector, RedisConsumer, RedisProducer, RedisCache

from app.tg_bot import TGBot
from app.config import Symbols, exchange_settings, PGSettings, RedisSettings, TGBotSettings
from app import AppLogger

__all__ = ["Application"]


class Application:
    def __init__(self):
        """
        Основной класс приложения, который настраивает все компоненты.
        """
        self.logger = AppLogger
        self.log = self.logger(name=type(self).__name__)

        self.db_connector = None
        self.redis_connector = None
        self.tg_bot = None
        self.distributor = None
        self.pg_pool_sessions = None

        self.repositories = RepositoryAggregator
        self.controllers = ControllerAggregator
        self.cache = RedisCache
        self.consumer = RedisConsumer
        self.producer = RedisProducer

        self.pg_settings = PGSettings()
        self.create_pg()
        self.create_redis()
        self.create_distributor()
        self.create_bot()

    async def launch(self):
        """
        Запустить launch_distributors и другое.
        Тут сначала будет выполняться подключение к бд, настройка кэша,
        запуск бота и другие необходимые компоненты, а уже после этого
        будет запуск DistributorAggregator, потому что он запускает основной
        процесс приложения - работа с биржами.
        :return:
        """

        self.tg_bot.redis_client = await self.redis_connector.connect()
        task_2 = asyncio.create_task(self.distributor.launch())
        task_3 = asyncio.create_task(self.tg_bot.launch())

        await asyncio.gather(task_3, task_2)

    def create_pg(self):
        self.log.debug("Создание и настройка postgres.")

        self.db_connector = PostgresConnector(
            user=self.pg_settings.USER,
            password=self.pg_settings.PASSWORD.get_secret_value(),
            db_name=self.pg_settings.DB_NAME,
            host=self.pg_settings.HOST,
            port=self.pg_settings.PORT,
            echo=self.pg_settings.ECHO,
            pool_size=self.pg_settings.POOL_SIZE,
            max_overflow=self.pg_settings.MAX_OVERFLOW,
        )
        self.pg_pool_sessions = self.db_connector.create_session()

    def create_redis(self):
        self.log.debug("Создание и настройка redis.")
        redis_settings = RedisSettings()

        self.redis_connector = RedisConnector(
            host=redis_settings.HOST,
            port=redis_settings.PORT,
            max_connections=redis_settings.MAX_CONNECTIONS,
            timeout=redis_settings.TIMEOUT,
            logger=self.logger
        )

    def create_distributor(self):
        self.log.debug("Создание дистрибьютора.")

        self.distributor = DistributorAggregator(
            symbols=Symbols().SYMBOLS,
            settings_list=exchange_settings,
            logger=self.logger
        )

    def create_bot(self):
        self.log.debug("Создание бота.")

        self.tg_bot = TGBot(
            token=TGBotSettings().TOKEN.get_secret_value(),
            controllers=self.controllers,
            redis_client=self.redis_connector.client,
            pg_session=self.pg_pool_sessions,
            cache=self.cache,
            repositories=self.repositories,
            logger=self.logger
        )




