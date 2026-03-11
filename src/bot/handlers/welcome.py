from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.ui.inline_kb import main_menu
from i18n.uz import UZ_TEXTS

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = await main_menu()
    await message.answer(UZ_TEXTS["start"], reply_markup=keyboard)


@router.message(F.photo)
async def answer_photo_id(message: Message):
    await message.answer(message.photo[-1].file_id)


@router.message(F.document)
async def answer_document_id(message: Message):
    await message.answer(message.document.file_id)