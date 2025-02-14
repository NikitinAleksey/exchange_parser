from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.tg_bot.services import create_inline_kb

__all__ = ["commands_router"]

commands_router = Router()


@commands_router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text=f"Привет, {message.from_user.id}. Ты успешно зарегистрирован. "
             "Теперь тебе будут приходить все уведомления.",
        reply_markup=create_inline_kb(
            buttons=...
        )
    )


