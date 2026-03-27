from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.db.database import DataBase
from src.i18n.uz import UZ_TEXTS
from src.bot.states.add import AddCategory
from src.db.repo.categories import CategoriesRepository
from src.bot.keyboards.inline import main_menu
from src.config.conf_logs import logger
from src.bot.handlers.categories import show_categories

router = Router()

@router.callback_query(F.data == "admin:c:add")
async def add_category(call: CallbackQuery, state: FSMContext, db: DataBase):
    await state.clear()
    await call.message.edit_text(UZ_TEXTS["admin:prompt_category_name"])
    await state.set_state(AddCategory.category_name)


@router.message(AddCategory.category_name)
async def prompt_category_name(message: Message, state: FSMContext, db: DataBase):
    categories_repo = CategoriesRepository(db)

    try:
        await categories_repo.add_category(message.text)
        await message.answer(UZ_TEXTS["admin:msg_category_added"], reply_markup=await main_menu(True))

    except Exception as e:
        logger.warning(e)
        await message.answer(UZ_TEXTS["error:db_error"])
        return

    finally:
        await state.clear()

@router.callback_query(F.data == "admin:c:edit")
async def add_category(call: CallbackQuery, state: FSMContext, db: DataBase):
    await state.clear()

    await show_categories(call, state, db, True)
    await state.set_state(AddCategory.c_id)


@router.callback_query(AddCategory.c_id, F.data.startswith("category:show:"))
async def add_category(call: CallbackQuery, state: FSMContext, db: DataBase):

    category_id = int(call.data.split(":")[-1])
    await state.update_data(c_id = category_id)
    await call.message.answer(UZ_TEXTS["admin:prompt_category_name_edit"])
    await state.set_state(AddCategory.c_name_upd)


@router.message(AddCategory.c_name_upd)
async def add_category(message: Message, state: FSMContext, db: DataBase):
    categories_repo = CategoriesRepository(db)
    data = await state.get_data()

    if "/" in message.text:
        await message.answer("'/' ishlatish mumkum emas!")
        return

    logger.info(f"data: {data}, c_name: {message.text}")
    await categories_repo.edit_category(message.text, data.get("c_id"))
    await state.clear()

    await message.answer(UZ_TEXTS["admin:msg_category_added"], reply_markup=await main_menu(True))
