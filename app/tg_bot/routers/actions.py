from aiogram import Router, F
from aiogram.types import CallbackQuery

__all__ = ["actions_router"]

actions_router = Router()


@actions_router.callback_query(F.data == "confirm")
async def confirm(callback: CallbackQuery):
    # Подтверждает действие (продажа, покупка)
    pass


@actions_router.callback_query(F.data == "reject")
async def reject(callback: CallbackQuery):
    # Отклоняет действие (продажа, покупка)
    pass


# TODO другие действия (например, запросить новости, запросить текущую выписку по кошелькам и т.д.)
