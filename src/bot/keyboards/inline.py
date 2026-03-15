from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from src.config.conf_logs import logger
from src.i18n.uz import UZ_BTNS

async def back_btn(builder: InlineKeyboardBuilder, to: str = "main"):

    btn = {}
    btn_txt = "⬅️"

    if to == "main":
        btn["menu:main"] = btn_txt

    elif to == "admin":
        btn["menu:admin"] = btn_txt

    elif to == "categories":
        btn["menu:categories"] = btn_txt

    for call_data, btn_text in btn.items():
        builder.button(
            text=btn_text,
            callback_data=call_data,
        )

async def main_menu(admin: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btns = UZ_BTNS["menu:main"]

    if admin:
        btns = UZ_BTNS["menu:admin"]


    for call, btn_text in btns.items():
        builder.button(
            text=btn_text,
            callback_data=call,
        )

    builder.adjust(2)
    return builder.as_markup()

async def books_keyboard(books: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for book in books:
        builder.button(
            text=f"📖 {book['book_name']}",
            callback_data=f"book:show:{book['id']}",
        )

    await back_btn(builder, "categories")

    builder.adjust(2)
    return builder.as_markup()


async def categories_keyboard(categories: list[dict], add: bool = False, to: str = "main") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    call = "category:show:"

    if add:
        call = "menu:category:show:"

    if len(categories) > 8:
        categories = categories[:-1]

    for category in categories:
        builder.button(
            text=f"📚 {category['category_name']}",
            callback_data=f"{call}{category['id']}",
        )

    await back_btn(builder, to)

    builder.adjust(2)
    return builder.as_markup()


async def authors_keyboard(authors: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for author in authors:
        builder.button(
            text=f"📚 {author['author_name']}",
            callback_data=f"author:{author['id']}",
        )

    builder.adjust(1)
    return builder.as_markup()