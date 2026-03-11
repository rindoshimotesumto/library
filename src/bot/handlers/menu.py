from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.ui.inline_kb import back_to_menu, show_book_list, show_category_list

from db.database import DataBase
from db.repo.books import BooksService
from db.repo.categories import CategoriesService

from i18n.uz import UZ_TEXTS

from core.states.search_book import SearchBook

router = Router()
db = DataBase()
books_service = BooksService(db)
categories_service = CategoriesService(db)


@router.callback_query(F.data.startswith("menu:"))
async def callback_h(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    categories = await categories_service.has_categories()
    books = await books_service.has_books()

    if not callback.data:
        return

    if not isinstance(callback.message, Message):
        return

    keyboard = await back_to_menu()
    call_data = callback.data.removeprefix("menu:")

    if call_data == "books":
        book_list = await books_service.get_books()
        next_book_id = None

        if book_list:
            if len(book_list) > 3:
                book_list = book_list[:-1]
                next_book_id = book_list[-1]["book_id"]
                
            books_kb = await show_book_list(book_list, next_book_id)
            await callback.message.answer(UZ_TEXTS["books:list"], reply_markup=books_kb)
            await callback.message.delete()
            return

        await callback.message.edit_text(UZ_TEXTS["no:books"], reply_markup=keyboard)

    elif call_data == "categories":
        if not categories:
            await callback.message.edit_text(UZ_TEXTS["no:categories"], reply_markup=keyboard)
            return
        
        next_categories_id = None
        categories_list = await categories_service.get_categories()
        
        if len(categories_list) > 3:
            categories_list = categories_list[:-1]
            next_categories_id = categories_list[-1]["category_id"]
            
        categories_kb = await show_category_list(categories_list, next_categories_id)
        await callback.message.edit_text(UZ_TEXTS["categories"], reply_markup=categories_kb)
            

    elif call_data == "search":
        if books:
            await callback.message.edit_text(UZ_TEXTS["search:prompt"], reply_markup=keyboard)
            await state.set_state(SearchBook.book_name)
            return

        await callback.message.edit_text(UZ_TEXTS["no:search"], reply_markup=keyboard)

    elif call_data == "profile":
        await callback.message.edit_text(UZ_TEXTS["no:profile"], reply_markup=keyboard)

    elif call_data == "help":
        await callback.message.edit_text(UZ_TEXTS["help"], reply_markup=keyboard)

    elif call_data == "settings":
        await callback.message.edit_text(UZ_TEXTS["no:settings"], reply_markup=keyboard)
