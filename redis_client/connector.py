import logging

import redis.asyncio as aioredis

__all__ = ["RedisConnector"]


class RedisConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
            self,
            host: str,
            port: int,
            max_connections: int,
            timeout: int,
            logger=None
    ):
        if not self._initialized:
            self.log = (logger(type(self).__name__)
                        if logger
                        else logging.getLogger(type(self).__name__))
            self.host = host
            self.port = port
            self.max_connections = max_connections
            self.timeout = timeout
            self.redis_url = self.url_builder()
            self.client = None
            self._initialized = True

    async def connect(self):
        """Создаёт подключение к Redis."""
        self.log.debug("Подключаемся к Редис.")

        self.client = await aioredis.from_url(
            self.redis_url,
            decode_responses=True,
            max_connections=self.max_connections,
            socket_connect_timeout=self.timeout
        )
        try:
            pong = await self.client.ping()
            self.log.debug(f"Redis ответил: {pong}")
            return self.client
        except Exception as exc:
            self.log.error(f"Не удалось подключиться к Redis. Ошибка: {exc}")
            raise


    async def close(self):
        """Закрывает соединение с Redis."""
        self.log.debug("Отключаемся от Редис.")

        if self.client:
            await self.client.close()

    def url_builder(self) -> str:
        """
        Создает ссылку для подключения к Redis.

        :return: Str - строка с URL для подключения.
        """
        self.log.debug("Строим ссылку для Редис.")

        return f"redis://{self.host}:{self.port}/"
