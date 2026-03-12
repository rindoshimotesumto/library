from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import books_keyboard, categories_keyboard
from src.db.repo.books import BookRepository

from src.db.repo.categories import CategoriesRepository
from src.db.database import DataBase

router = Router()


@router.callback_query(F.data == "menu:categories")
async def show_categories(callback: CallbackQuery, state: FSMContext, db: DataBase):
    await callback.answer()

    categories_repository = CategoriesRepository(db)
    categories = await categories_repository.get_categories()
    categories_kb = await categories_keyboard(categories, True)

    await callback.message.edit_text(UZ_TEXTS["admin:btn_categories"], reply_markup=categories_kb)


@router.callback_query(F.data.startswith("menu:category:show:"))
async def show_category_books(callback: CallbackQuery, state: FSMContext, db: DataBase):
    await callback.answer()

    category_id = int(callback.data.removeprefix("menu:category:show:"))

    book_repository = BookRepository(db)
    books = await book_repository.get_books_category(category_id)
    books_kb = await books_keyboard(books)

    await callback.message.edit_text(UZ_TEXTS["book:list_title"], reply_markup=books_kb)