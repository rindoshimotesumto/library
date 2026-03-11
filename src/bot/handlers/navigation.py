from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from i18n.uz import UZ_TEXTS

from bot.ui.inline_kb import main_menu
from bot.ui.inline_kb import show_book_list

from db.database import DataBase
from db.repo.books import BooksService

router = Router()
db = DataBase()
books_service = BooksService(db)


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
    

@router.callback_query(F.data.startswith("prev:"))
async def click_prev_btns(callback: CallbackQuery):
    await callback.answer()
    call_data = callback.data.removeprefix("prev:")
    
    next_book_page = None
    prev_book_page = None
    
    if call_data.startswith("books:"):
        prev_book_id = int(call_data.removeprefix("books:"))
        book_list = await books_service.get_books(prev_book_id)
        max_task_id = await books_service.get_max_id()
        if book_list:
            if book_list[0]["book_id"] > max_task_id["book_id"]:
                prev_book_page = book_list[-1]["book_id"]
                
            next_book_page = book_list[0]["book_id"] + 1
        
            if len(book_list) > 3:
                book_list = book_list[:-1]
                
        
        books_kb = await show_book_list(book_list, next_book_page, prev_book_page)
        await callback.message.edit_text(UZ_TEXTS["books:list"], reply_markup=books_kb)
    
    
@router.callback_query(F.data.startswith("back:"))
async def click_back_btns(callback: CallbackQuery):
    await callback.answer()
    call_data = callback.data.removeprefix("back:")
        
    if call_data.startswith("menu"):
        keyboard = await main_menu()
    
        if not isinstance(callback.message, Message):
            return
    
        await callback.message.edit_text(UZ_TEXTS["start"], reply_markup=keyboard)