import logging

from aiogram import Dispatcher, Bot
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.tg_bot.routers import routers
from app.tg_bot.middlewares import middlewares
from app.controllers import ControllerAggregator

__all__ = ["TGBot"]

from database import RepositoryAggregator

from redis_client import RedisConnector, RedisCache


class TGBot:
    def __init__(
            self,
            token: str,
            controllers: type[ControllerAggregator],
            pg_session: AsyncSession,
            redis_client: Redis,
            cache: type[RedisCache],
            repositories: type[RepositoryAggregator],
            logger=None
    ):
        """
        Основной класс ТГ бота, который:
        - создает объекты диспетчера и бота;
        - регистрирует роутеры и миддлвари;
        - запускает бота.

        :param token: Расшифрованный токен для бота.
        """
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.routers = routers
        self.middlewares = middlewares
        self.controllers = controllers
        self.repositories = repositories
        self.cache = cache
        self.redis_client = redis_client
        self.pg_session = pg_session
        self.logger = logger
        self.log = (self.logger (type(self).__name__)
                    if self.logger
                    else logging.getLogger(type(self).__name__))

    def register_all_routers(self):
        """
        Регистрирует все роутеры в диспетчере из списка routers.
        Все существующие роутеры должны быть импортированы и добавлены
        в routers.
        """
        self.log.debug("Регистрируем маршруты.")

        for router in self.routers:
            self.dp.include_router(router=router)

    def register_all_middleware(self):
        """
        Регистрирует все миддлвари в диспетчере из списка middlewares.
        Все существующие миддлвари должны быть импортированы и добавлены
        в middlewares.
        """
        self.log.debug("Регистрируем миддлвари.")

        for middleware in self.middlewares:
            self.dp.update.middleware(
                middleware(
                    controllers=self.controllers,
                    cache=self.cache,
                    redis_client=self.redis_client,
                    pg_session=self.pg_session,
                    repositories=self.repositories,
                    logger=self.logger
                )
            )

    async def launch(self):
        """Запускает бота с указанными параметрами."""
        self.log.debug("Запускаем регистрацию компонентов.")

        self.register_all_routers()
        self.register_all_middleware()
        self.log.debug("Успех, запускаем бота.")

        await self.dp.start_polling(self.bot)
