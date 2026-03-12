from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import main_menu

from src.db.database import DataBase

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state:FSMContext, db: DataBase):
    await state.clear()
    await message.answer(UZ_TEXTS["common:start"], reply_markup=await main_menu(False))

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext, db: DataBase):
    await state.clear()
    await message.answer(UZ_TEXTS["common:start"], reply_markup=await main_menu(True))

# @router.message(F.photo)
# async def cmd_photo(message: Message, db: DataBase):
#     await message.answer(message.photo[-1].file_id)
#
# @router.message(F.document)
# async def cmd_document(message: Message, db: DataBase):
#     await message.answer(message.document.file_id)