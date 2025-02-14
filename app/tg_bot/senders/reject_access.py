import random

from aiogram.types import TelegramObject

__all__ = ["reject_access"]


async def reject_access(
        event: TelegramObject,
):
    text = random.choice(
        [
            "У тебя нет доступа, ступай дальше. Удачи!",
            "Ты, конечно, попытался... Но нет. Иди поплачь в угол.",
            "Ты кто такой? Я тебя не звал, иди ты на**й!",
            "Ты так и не понял? Проваливай!",
            "Не приходите в мой дом. Мои двери закрыты.",
        ]
    )
    message = None
    if hasattr(event, 'message') and event.message is not None:
        message = event.message
    elif hasattr(event, 'callback_query') and event.callback_query is not None:
        message = event.callback_query.message

    await message.answer(
        text=text
    )
