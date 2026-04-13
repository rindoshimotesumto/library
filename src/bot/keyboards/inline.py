from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from dataclasses import dataclass
from src.config.conf_logs import logger
from src.i18n.uz import UZ_BTNS, UZ_TEXTS

@dataclass
class ChanellInfo:
    channel_id: int
    channel_url: str
    channel_name: str

async def more_btn(builder: InlineKeyboardBuilder, b_id: int, c_id: int, like: bool = False):
    if like:
        builder.button(
            text=UZ_BTNS["book_actions"]["liked"],
            callback_data=f"book:show:liked:{c_id}:{b_id}",
        )

    elif not like:
        builder.button(
            text=UZ_BTNS["book_actions"]["like"],
            callback_data=f"book:show:like:{c_id}:{b_id}",
        )

async def next_btn(builder: InlineKeyboardBuilder, to: str, c_id: int, book_id: int) -> None:

    btn = {}
    btn_text = "➡️"

    if to == "books":
        btn[f"menu:c:sh:{c_id}:{book_id}"] = btn_text

    for k, v in btn.items():
        builder.button(
            text=k,
            callback_data=k
        )

async def back_btn(builder: InlineKeyboardBuilder, to: str = "main", c_id: int = None, b_id: int = None):

    btn = {}
    btn_txt = "⬅️"

    if to == "main":
        btn["menu:main"] = btn_txt

    elif to == "admin":
        btn["menu:admin"] = btn_txt

    elif to == "categories":
        btn["menu:categories"] = btn_txt

    elif to == "books":
        if isinstance(c_id, int):
            if isinstance(b_id, int):
                btn[f"menu:c:sh:{c_id}:{b_id}"] = btn_txt
            else:
                btn[f"menu:c:sh:{c_id}"] = btn_txt

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

async def books_keyboard(
    books: list[dict],
    category_id: int,
    page_count: int,
    c_page: int = 1,
    show_book_id: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for book in books:
        if show_book_id:
            builder.button(
                text=f"📖 {book['book_name']} [{book['id']}]",
                callback_data=f"book:show:{book['id']}",
            )
        else:
            builder.button(
                text=f"📖 {book['book_name']}",
                callback_data=f"book:show:{book['id']}",
            )

    first_book_id = books[0]["id"]
    last_book_id = books[-1]["id"]

    # Назад
    if c_page == 1:
        await back_btn(builder, "categories")
    else:
        builder.button(
            text="⬅️",
            callback_data=f"menu:c:sh:{category_id}:prev:{first_book_id}"
        )

    # Текущая страница
    builder.button(
        text=f"{c_page} / {page_count}",
        callback_data="ignore",
    )

    # Вперед
    if c_page != page_count:
        builder.button(
            text="➡️",
            callback_data=f"menu:c:sh:{category_id}:next:{last_book_id}"
        )

    builder.adjust(*([1] * len(books)), 3)
    return builder.as_markup()


async def categories_keyboard(
    categories: list[dict],
    page_count: int = 1,
    c_page: int = 1,
    to: str = "main",
    add: bool = False,
    admin: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if add:
        call_data = "category:show:"

    else:
        call_data = "menu:c:sh:"

    _ = {
        1: '🌍', 2: '⭐', 3: '🕵️', 4: '🌸', 5: '👤', 6: '🏛️',
        7: '🚀', 8: '📖', 9: '🏛️', 10: '🔬', 11: '😏', 12: '🧭',
        13: '🧸', 15: '🌱', 16: '🧠', 17: '💼', 19: '🎧'
    }

    for category in categories:
        if admin is True or add is True:
            builder.button(
                text=f"{_.get(category['id'], "📚")} {category['category_name']} ({category['book_count']}ta)",
                callback_data=f"{call_data}{category['id']}",
            )

        else:
            builder.button(
                text=f"{_.get(category['id'], "📚")} {category['category_name']}",
                callback_data=f"{call_data}{category['id']}",
            )

    first_category_id = categories[0]["id"]
    last_category_id = categories[-1]["id"]

    if c_page == 1:
        if add:
            to = "admin"

        await back_btn(builder, to)
    else:
        builder.button(
            text="⬅️",
            callback_data=f"menu:categories:prev:{first_category_id}",
        )

    builder.button(
        text=f"{c_page} / {page_count}",
        callback_data="ignore",
    )

    if c_page != page_count:
        builder.button(
            text="➡️",
            callback_data=f"menu:categories:next:{last_category_id}",
        )

    builder.adjust(*([1] * len(categories)), 3)
    return builder.as_markup()



async def authors_keyboard(
    authors: list[dict],
    page_count: int,
    c_page: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for author in authors:
        builder.button(
            text=f"📚 {author['author_name']}",
            callback_data=f"author:{author['id']}",
        )

    first_id = authors[0]["id"]
    last_id = authors[-1]["id"]

    # ⬅️
    if c_page == 1:
        builder.button(text="⬅️", callback_data="admin:b:add")
    else:
        builder.button(
            text="⬅️",
            callback_data=f"author:prev:{first_id}"
        )

    builder.button(
        text=f"{c_page} / {page_count}",
        callback_data="ignore"
    )

    # ➡️
    if c_page != page_count:
        builder.button(
            text="➡️",
            callback_data=f"author:next:{last_id}"
        )

    builder.adjust(*([1] * len(authors)), 3)
    return builder.as_markup()

async def get_sub_keyboard(chanells_info: list[ChanellInfo]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for channel in chanells_info:
        builder.row(InlineKeyboardButton(
            text=channel.channel_name,
            url=channel.channel_url)
        )

    builder.row(InlineKeyboardButton(
        text=UZ_TEXTS["sub:button_check"],
        callback_data="check_sub")
    )
    return builder.as_markup()