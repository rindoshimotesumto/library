from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.ui.inline_kb import main_menu
from i18n.uz import UZ_TEXTS

from db.database import DataBase
from db.repo.users import UsersService

router = Router()
db = DataBase()
users_service = UsersService(db)

@router.message(Command("admin"))
async def cmd_admin(message: Message):

    user_role = await users_service.get_role(message.from_user.id)

    if user_role["role"] != "admin":
        await message.answer(UZ_TEXTS["access:denied"])
        return

    keyboard = await main_menu("admin")
    await message.answer(UZ_TEXTS["admin:panel"], reply_markup=keyboard)


@router.callback_query(F.data.startswith("admin:"))
async def admin_handler(callback: CallbackQuery):
    await callback.answer()

    call_data = callback.data.removeprefix("admin:")

    if call_data.startswith("add:"):
        add_info_type = call_data.removeprefix("add:")

        if add_info_type == "book":
            ...

        elif add_info_type == "category":
            ...

    elif call_data.startswith("delete:"):
        delete_info_type = call_data.removeprefix("delete:")

        if delete_info_type == "book":
            ...

        elif delete_info_type == "category":
            ...

    elif call_data.startswith("edit:"):
        edit_info_type = call_data.removeprefix("edit:")

        if edit_info_type == "book":
            ...

        elif edit_info_type == "category":
            ...