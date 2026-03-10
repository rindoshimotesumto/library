from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.ui.inline_kb import main_menu
from i18n.uz import UZ_TEXTS

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = await main_menu()
    await message.answer(UZ_TEXTS["start"], reply_markup=keyboard)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    keyboard = await main_menu("admin")
    await message.answer(UZ_TEXTS["admin:panel"], reply_markup=keyboard)