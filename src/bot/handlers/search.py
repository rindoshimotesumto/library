from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from db.database import DataBase
from db.repo.books import BooksService
from i18n.uz import UZ_TEXTS

from core.states.search_book import SearchBook
from bot.ui.inline_kb import show_book_list

router = Router()
db = DataBase()
books_service = BooksService(db)


@router.message(SearchBook.book_name)
async def search_book(message: Message, state: FSMContext):
    
    if not message.text:
        return
        
    book_list = await books_service.search_book(message.text.strip().title())
    
    if not book_list:
        return
        
    books_keyboard = await show_book_list(book_list)
    await message.answer(text=UZ_TEXTS["search:results"], reply_markup=books_keyboard)
    await message.delete()
    await state.clear()