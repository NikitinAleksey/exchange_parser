from typing import Union

from redis.asyncio import Redis

from app import AppLogger

__all__ = ["RedisCache"]


class RedisCache:
    def __init__(self, redis_client: Redis, logger: AppLogger):
        self.client = redis_client

    async def get(self, key: str):
        """Получить данные из кэша."""
        return await self.client.get(key)

    async def get_allowed_users(self):
        return await self.client.smembers("allowed_users")

    async def set(self, key: str, value: str):
        """Записать данные в кэш."""
        await self.client.set(key, value)

    async def set_allowed_users(self, users_id: Union[list, tuple, set]):
        return await self.client.sadd("allowed_users", *users_id)

    async def delete(self, key: str):
        """Удалить данные из кэша."""
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Проверить, есть ли ключ в кэше."""
        return await self.client.exists(key) > 0
