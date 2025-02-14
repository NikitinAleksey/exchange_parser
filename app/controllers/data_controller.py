from sqlalchemy.ext.asyncio import AsyncSession

from database import RepositoryAggregator
from database.pg_connector import PostgresConnector
from redis_client import RedisCache
from redis.asyncio import Redis
from database.repository.base import BaseRepository


__all__ = ["DataController"]


class DataController:
    def __init__(
            self,
            cache: type[RedisCache],
            redis_client: Redis,
            repositories: type[RepositoryAggregator],
            pg_session: AsyncSession,
            logger=None
    ):
        self.log = logger(name=type(self).__name__)
        self.cache = cache(redis_client=redis_client, logger=logger)
        self.pg_session = pg_session
        self.repository = repositories

    async def get(self, key: str):
        """С помощью репозитория делает запрос к кжшу, если там пусто, то идет к бд, на обратном пути записывает данные в кэш"""
        ...

    async def get_all_users(self):
        self.log.debug("Запрос списка разрешенных пользователей.")

        allowed_users = await self.cache.get_allowed_users()
        if allowed_users is None:
            self.log.debug("В кэше нет пользователей. Запрос к бд.")
            allowed_users = await self.repository.user.get_all_users(
                session=self.pg_session
            )
            allowed_users = set(allowed_users)

            self.log.debug("Пользователи получены. Обновляем кэш.")
            await self.cache.set_allowed_users(
                users_id=allowed_users
            )
        self.log.debug("Возвращаем пользователей.")
        return allowed_users

    async def set(self):
        """Обновляет, записывает данные в бд, удаляет неактуальные из кжша."""
        ...


# TODO  AttributeError: 'NoneType' object has no attribute 'smembers'
#  Редис голову ебет, разобраться.