from typing import Optional

from aiogram import Bot

from app.tg_bot.services import create_inline_kb

__all__ = ["send_notification"]


async def send_notification(
        bot: Bot,
        text: str,
        user_id: int,
        buttons: list[list],
        adjust: Optional[int]
):
    await bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=create_inline_kb(
            buttons=buttons,
            adjust=adjust if adjust else 2
        )
    )
