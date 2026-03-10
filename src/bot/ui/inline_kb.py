from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from i18n.uz import UZ_BTNS

async def main_menu(role: str = "user") -> InlineKeyboardMarkup:
    """
    Generate main menu.
    """
    
    builder = InlineKeyboardBuilder()
    btns = UZ_BTNS["main_menu"]
    
    if role == "admin":
       btns =  UZ_BTNS["admin_panel"]
    
    for data, btn_text in btns.items():
        builder.row(
            InlineKeyboardButton(text=btn_text, callback_data=data)
        )
    
    builder.adjust(2)
    return builder.as_markup()
    
    
async def back_to_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=UZ_BTNS["navigation_menu"]["back"], callback_data="back:menu")
    )
    
    builder.adjust(1)
    return builder.as_markup()


async def back_to_book_list(book_file_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text=UZ_BTNS["navigation_menu"]["back"], callback_data="menu:books")
    )

    builder.row(
        InlineKeyboardButton(text=UZ_BTNS["get_book"]["book:download"], callback_data=f"book:download:{book_file_id}")
    )

    builder.adjust(2)
    return builder.as_markup()
    

async def show_book_list(book_list: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for book in book_list:

        builder.row(
            InlineKeyboardButton(text=f"📖 {book['book_name']}", callback_data=f"book:id:{book['book_id']}")
        )

    builder.row(
        InlineKeyboardButton(text=UZ_BTNS["navigation_menu"]["back"], callback_data="back:menu")
    )

    builder.adjust(*([1]*len(book_list)), 2)
    return builder.as_markup()