"""
Здесь необходимо регистрировать все роутеры бота.
Просто импортировать и добавить в список.
"""
from app.tg_bot.routers.commands import commands_router
from app.tg_bot.routers.actions import actions_router

__all__ = ["routers"]

routers = [commands_router, actions_router]
