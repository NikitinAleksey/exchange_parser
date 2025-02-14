"""
Здесь необходимо регистрировать все миддлвари бота.
Просто импортировать и добавить в список.
"""
from app.tg_bot.middlewares.autentification import AuthMiddleware

__all__ = ["middlewares"]

middlewares = [
    AuthMiddleware
]
