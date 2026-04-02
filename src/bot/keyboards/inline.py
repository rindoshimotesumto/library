from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from src.i18n.i18n import Langs, t, MAIN_MSG_BTNS

async def menu(lang: Langs | str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for btn in MAIN_MSG_BTNS:
        btn_txt = t(btn, lang)

        builder.button(
            text=btn_txt,
            callback_data=btn,
        )

    builder.adjust(2)
    return builder.as_markup()