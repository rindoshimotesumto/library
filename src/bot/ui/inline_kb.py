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
    

async def show_info_list(info_list: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    info_count = 0
    
    # кб для показа информации ввиде кнопок
    
    builder.adjust(*([1]*info_count), 2)
    return builder.as_markup()