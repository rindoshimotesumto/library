from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.config.conf_logs import logger
from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import books_keyboard, categories_keyboard

from src.db.repo.books import BookRepository
from src.db.repo.categories import CategoriesRepository
from src.db.repo.users import UsersRepository
from src.db.database import DataBase

router = Router()

@router.callback_query(F.data.startswith("menu:categories"))
async def show_categories(callback: CallbackQuery, state: FSMContext, db: DataBase, admin: bool = False):
    await callback.answer()

    users_repo = UsersRepository(db)
    user_is_admin = await users_repo.get_user(callback.from_user.id)

    if user_is_admin.role == "admin":
        user_is_admin = True
    else:
        user_is_admin = False

    data = await state.get_data()
    current_page = data.get("categories_current_page", 1)

    direction = None
    cursor_id = None

    if callback.data != "menu:categories":
        payload = callback.data.removeprefix("menu:categories:").split(":")
        if len(payload) == 2:
            direction = payload[0]
            cursor_id = int(payload[1])

    categories_repository = CategoriesRepository(db)

    page_count = await categories_repository.get_categories_page_count(page_size=9)
    categories = await categories_repository.get_categories(
        cursor_id=cursor_id,
        page_size=9,
        direction=direction or "next",
        admin=user_is_admin
    )

    if not categories:
        await callback.answer("-", show_alert=False)
        return

    if direction == "next":
        current_page += 1
    elif direction == "prev":
        current_page = max(1, current_page - 1)
    else:
        current_page = 1

    await state.update_data(categories_current_page=current_page)

    categories_kb = await categories_keyboard(
        categories=categories,
        page_count=page_count,
        c_page=current_page,
        add=admin,
        admin=user_is_admin
    )

    try:
        await callback.message.edit_text(
            UZ_TEXTS["admin:btn_categories"],
            reply_markup=categories_kb,
        )
    except Exception as e:
        logger.exception(e)
        await callback.message.answer(
            UZ_TEXTS["admin:btn_categories"],
            reply_markup=categories_kb,
        )
        await callback.message.delete()


@router.callback_query(F.data.startswith("menu:c:sh:"))
async def show_category_books(callback: CallbackQuery, state: FSMContext, db: DataBase):
    await callback.answer()
    data = await state.get_data()

    current_page = data.get("current_page", 1)

    payload = callback.data.removeprefix("menu:c:sh:").split(":")
    category_id = int(payload[0])

    direction = None
    cursor_id = None

    if len(payload) == 3:
        direction = payload[1]
        cursor_id = int(payload[2])

    book_repository = BookRepository(db)
    books_count = await book_repository.get_books_page_count(category_id)
    books = await book_repository.get_books_category(
        category_id=category_id,
        cursor_id=cursor_id,
        direction=direction or "next",
        page_size=10,
    )

    if not books:
        await callback.answer("-", show_alert=False)
        return

    # books = books[:9]

    if direction == "next":
        current_page += 1
    elif direction == "prev":
        current_page = max(1, current_page - 1)
    else:
        current_page = 1

    await state.update_data(current_page=current_page)

    books_kb = await books_keyboard(
        books=books,
        category_id=category_id,
        page_count=books_count,
        c_page=current_page,
    )

    try:
        await callback.message.edit_text(
            UZ_TEXTS["book:list_title"],
            reply_markup=books_kb
        )
    except Exception as e:
        logger.exception(e)
        await callback.message.answer(
            UZ_TEXTS["book:list_title"],
            reply_markup=books_kb
        )
        await callback.message.delete()