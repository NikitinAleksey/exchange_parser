from contextlib import asynccontextmanager
from typing import AsyncIterator
from urllib.parse import quote_plus
import logging

from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.ext.asyncio import async_sessionmaker

__all__ = ["PostgresConnector"]


class PostgresConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
            self,
            user: str,
            password: str,
            db_name: str,
            host: str,
            port: int,
            echo: bool,
            pool_size: int,
            max_overflow: int,
            logger=None
    ):
        if not self._initialized:
            self.log = (logger(type(self).__name__)
                        if logger
                        else logging.getLogger(type(self).__name__))
            self.user = user
            self.password = password
            self.db_name = db_name
            self.host = host
            self.port = port
            self.echo = echo
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.db_url = self.url_builder()
            self.engine = self.create_engine()
            self.async_session = self.create_session()
            self._initialized = True

    def url_builder(self) -> str:
        """
        Создает ссылку для подключения к базе данных.

        :return: Str - строка с URL для подключения.
        """
        self.log.debug("Собираем url для постгрес.")
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:"
            f"{quote_plus(self.password)}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.db_name}"
        )

    def create_engine(self) -> AsyncEngine:
        """
        Создает и возвращает движок для работы с базой данных.

        :return: AsyncEngine - движок SQLAlchemy для асинхронной работы.
        """
        self.log.debug("Создаем движок для постгрес.")

        return create_async_engine(
            self.db_url,
            echo=self.echo,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
        )

    def create_session(self) -> async_sessionmaker[AsyncSession]:
        """
        Создает пул сессий для работы с базой данных.

        :return: Sessionmaker - фабрика сессий для асинхронной работы с базой данных.
        """
        self.log.debug("Создаем пул сессий для постгрес.")

        return async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """
        Возвращает объект сессии из пула.

        :return: AsyncSession - объект сессии для выполнения запросов.
        """
        self.log.debug("Отдаем сессию из пула.")

        async with self.async_session() as session:
            yield session
