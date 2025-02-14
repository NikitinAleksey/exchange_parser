from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.controllers import ControllerAggregator
from app.tg_bot.senders import reject_access
from database import RepositoryAggregator

__all__ = ["AuthMiddleware"]

from redis_client import RedisCache


class AuthMiddleware(BaseMiddleware):
    """
    Миддлвари для аутентификации.
    Если пользователя нет в бд, отправит ему это.
    В противном случае - работает штатно.
    """
    def __init__(
            self,
            controllers: type[ControllerAggregator],
            repositories: type[RepositoryAggregator],
            cache: RedisCache,
            redis_client: Redis,
            pg_session: async_sessionmaker[AsyncSession],
            logger
    ):
        self.log = logger(name=type(self).__name__)
        self.data_controller = controllers.data(
            cache=cache,
            redis_client=redis_client,
            pg_session=pg_session,
            repositories=repositories,
            logger=logger
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if hasattr(event, 'message') and event.message is not None:
            user_id = event.message.from_user.id
        elif hasattr(event, 'callback_query') and event.callback_query is not None:
            user_id = event.callback_query.from_user.id
        else:
            self.log.warning(f"Не удалось получить айди при событии: "
                             f"{type(event)}")
            user_id = -1

        if not int(user_id) in await self.data_controller.get_all_users():
            return await reject_access(
                event=event
            )
        return await handler(event, data)
