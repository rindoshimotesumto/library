from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from i18n.uz import UZ_TEXTS

from bot.ui.inline_kb import main_menu, show_category_list
from bot.ui.inline_kb import show_book_list

from db.database import DataBase
from db.repo.books import BooksService
from db.repo.categories import CategoriesService

router = Router()
db = DataBase()
books_service = BooksService(db)
categories_service = CategoriesService(db)


@router.callback_query(F.data.startswith("next:"))
async def click_next_btn(callback: CallbackQuery):
    await callback.answer()
    call_data = callback.data.removeprefix("next:")
    
    if call_data.startswith("book:"):
        next_book_id = int(call_data.removeprefix("book:"))
        book_list = await books_service.get_books(next_book_id)
        next_book_page = None
        prev_book_page = None
        
        if len(book_list) > 3:
            book_list = book_list[:-1]
            next_book_page = book_list[-1]["book_id"]
        
        prev_book_page = book_list[-1]["book_id"]
        books_kb = await show_book_list(book_list, next_book_page, prev_book_page)
        await callback.message.edit_text(UZ_TEXTS["books:list"], reply_markup=books_kb)
        
    elif call_data.startswith("category:"):
        next_category_id = int(call_data.removeprefix("category:"))
        category_list = await categories_service.get_categories(next_category_id)
        next_category_page = None
        prev_category_page = None
        
        if len(category_list) > 3:
            category_list = category_list[:-1]
            next_category_page = category_list[-1]["category_id"]
        
        prev_category_page = category_list[-1]["category_id"]
        category_kb = await show_category_list(category_list, next_category_page, prev_category_page)
        await callback.message.edit_text(UZ_TEXTS["categories"], reply_markup=category_kb)
    

@router.callback_query(F.data.startswith("prev:"))
async def click_prev_btns(callback: CallbackQuery):
    await callback.answer()
    call_data = callback.data.removeprefix("prev:")
    
    next_book_page = None
    prev_book_page = None
    next_category_page = None
    prev_category_page = None
    
    if call_data.startswith("books:"):
        prev_book_id = int(call_data.removeprefix("books:"))
        book_list = await books_service.get_books(prev_book_id)
        max_book_id = await books_service.get_max_id()
        if book_list:
            if book_list[0]["book_id"] > max_book_id["book_id"]:
                prev_book_page = book_list[-1]["book_id"]
                
            next_book_page = book_list[0]["book_id"] + 1
        
            if len(book_list) > 3:
                book_list = book_list[:-1]
        
        books_kb = await show_book_list(book_list, next_book_page, prev_book_page)
        await callback.message.edit_text(UZ_TEXTS["books:list"], reply_markup=books_kb)
        
    elif call_data.startswith("category:"):
        prev_category_id = int(call_data.removeprefix("category:"))
        category_list = await categories_service.get_categories(prev_category_id)
        max_category_id = await categories_service.get_max_id()
        
        if category_list:
            if category_list[0]["category_id"] > max_category_id["category_id"]:
                prev_category_page = category_list[-1]["category_id"]
                
            next_category_page = category_list[0]["category_id"] + 1
        
            if len(category_list) > 3:
                category_list = category_list[:-1]
        
        category_kb = await show_category_list(category_list, next_category_page, prev_category_page)
        await callback.message.edit_text(UZ_TEXTS["books:list"], reply_markup=category_kb)
    
    
@router.callback_query(F.data.startswith("back:"))
async def click_back_btns(callback: CallbackQuery):
    await callback.answer()
    call_data = callback.data.removeprefix("back:")
        
    if call_data.startswith("menu"):
        keyboard = await main_menu()
    
        if not isinstance(callback.message, Message):
            return
    
        await callback.message.edit_text(UZ_TEXTS["start"], reply_markup=keyboard)