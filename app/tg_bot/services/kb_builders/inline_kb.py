from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = ["create_inline_kb"]


def create_inline_kb(buttons: list[list], adjust: int = 2):
    """
    Создает клавиатуру с заданными кнопками и настройками.

    :param buttons: Список кнопок, каждая кнопка представлена
                    списком с текстом и callback_data.
    :param adjust: Количество колонок для кнопок в клавиатуре.
    :return: Инлайн клавиатура в виде разметки.
    """
    builder = InlineKeyboardBuilder()
    create_buttons(buttons=buttons, builder=builder)
    builder.adjust(adjust)
    return builder.as_markup()


def create_buttons(buttons: list[list[str]], builder: InlineKeyboardBuilder) -> None:
    """
    Создает кнопки для клавиатуры.

    :param buttons: Список кнопок, каждая кнопка представлена
                    списком с текстом и callback_data.
    :param builder: Объект для построения клавиатуры.
    :return: None
    """
    for button in buttons:
        builder.button(text=button[0], callback_data=button[1])
