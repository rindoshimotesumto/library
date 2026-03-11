from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from i18n.uz import UZ_BTNS, UZ_TEXTS

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
        InlineKeyboardButton(text=UZ_TEXTS["book:read"], callback_data="book:read")
    )
    
    builder.row(
        InlineKeyboardButton(text=UZ_TEXTS["book:like"], callback_data="book:like")
    )
    
    builder.row(
        InlineKeyboardButton(text=UZ_BTNS["navigation_menu"]["back"], callback_data="menu:books")
    )

    builder.row(
        InlineKeyboardButton(text=UZ_BTNS["get_book"]["book:download"], callback_data=f"book:download:{book_file_id}")
    )

    builder.adjust(2)
    return builder.as_markup()
    

async def show_book_list(book_list: list[dict], next_book_id: int | None = None, prev_book_id: int | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for book in book_list:
        builder.row(
            InlineKeyboardButton(text=f"📖 {book['book_name']}", callback_data=f"book:id:{book['book_id']}")
        )
        
    back_btn_call = "back:menu"
    txt = UZ_BTNS["navigation_menu"]["back"]
    
    if isinstance(prev_book_id, int):
        back_btn_call = f"prev:books:{prev_book_id}"
        txt = UZ_BTNS["navigation_menu"]["previous"]

    builder.row(
        InlineKeyboardButton(text=txt, callback_data=back_btn_call)
    )
    
    if isinstance(next_book_id, int):
        builder.row(
            InlineKeyboardButton(text=UZ_BTNS["navigation_menu"]["next"], callback_data=f"next:book:{next_book_id}")
        )
        
    builder.adjust(*([1]*len(book_list)), 2)
    return builder.as_markup()
    
    
async def show_category_list(category_list: list[dict], next_category_id: int | None = None, prev_category_id: int | None = None):
    builder = InlineKeyboardBuilder()
    
    
    for category in category_list:
        builder.row(
            InlineKeyboardButton(text=f"📚 {category['category_name']}", callback_data=f"category:id:{category['category_id']}")
        )
        
    back_btn_call = "back:menu"
    txt = UZ_BTNS["navigation_menu"]["back"]
    
    if isinstance(prev_category_id, int):
        back_btn_call = f"prev:category:{prev_category_id}"
        txt = UZ_BTNS["navigation_menu"]["previous"]

    builder.row(
        InlineKeyboardButton(text=txt, callback_data=back_btn_call)
    )
    
    if isinstance(next_category_id, int):
        builder.row(
            InlineKeyboardButton(text=UZ_BTNS["navigation_menu"]["next"], callback_data=f"next:category:{next_category_id}")
        )
    
    
    builder.adjust(*([1]*len(category_list)), 2)
    return builder.as_markup()