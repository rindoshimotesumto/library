from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

from src.i18n.i18n import Langs, t, MAIN_MSG_BTNS, CHECK_SUBSCRIBE_BTN, DEFAULT_LANG
from src.data.repo.mandatory_channels import ChannelsType
from src.data.repo.categories import CategoriesType
from pydantic import validate_call

@validate_call
async def menu_kb(lang: Langs = DEFAULT_LANG) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for btn in MAIN_MSG_BTNS:
        btn_txt = t(btn, lang)

        builder.button(
            text=btn_txt,
            callback_data=btn,
        )

    builder.adjust(2)
    return builder.as_markup()

@validate_call
async def check_sub_kb(chats: list[ChannelsType], lang: Langs = DEFAULT_LANG) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for chat in chats:
        btn_txt = chat.title
        btn_call = str(chat.chat_id)
        btn_url = chat.invite_link

        builder.button(
            text=btn_txt,
            callback_data=btn_call,
            url=btn_url,
        )

    builder.button(
        text=t(CHECK_SUBSCRIBE_BTN, lang.value),
        callback_data=CHECK_SUBSCRIBE_BTN
    )

    builder.adjust(1)
    return builder.as_markup()

@validate_call
async def category_kb(
        categories: list[CategoriesType],
        lang: Langs = DEFAULT_LANG,
        prev_category_id: int = None,
        next_category_id: int = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for cat in categories:
        builder.button(
            text=cat.name,
            callback_data="category:cat.id",
        )

    builder.adjust(1)
    return builder.as_markup()