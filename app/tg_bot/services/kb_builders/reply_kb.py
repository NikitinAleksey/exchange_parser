from aiogram.utils.keyboard import ReplyKeyboardBuilder

__all__ = ["create_reply_kb"]


def create_reply_kb(buttons: list[str], adjust: int = 2):
    """
    Создает клавиатуру с заданными кнопками.

    :param buttons: - список строк с текстами для кнопок.
    :param adjust: Количество колонок для кнопок в клавиатуре.
    :return: Реплай клавиатура в виде разметки.
    """
    builder = ReplyKeyboardBuilder()
    create_buttons(buttons=buttons, builder=builder)
    builder.adjust(adjust)
    return builder.as_markup()


def create_buttons(buttons: list[str], builder: ReplyKeyboardBuilder):
    """
    Создает кнопки для клавиатуры.

    :param buttons: Список строк с текстами для кнопок.
    :param builder: ReplyKeyboardBuilder - объект для построения клавиатуры.
    """
    for button in buttons:
        builder.button(text=button)
