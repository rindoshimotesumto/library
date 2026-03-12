from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from src.i18n.uz import UZ_BTNS

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

    builder.adjust(1)
    return builder.as_markup()


async def categories_keyboard(categories: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(
            text=f"📚 {category['category_name']}",
            callback_data=f"category:show:{category['id']}",
        )

    builder.adjust(1)
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