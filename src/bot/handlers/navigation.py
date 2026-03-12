from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import books_keyboard
from src.db.repo.books import BookRepository
from src.db.database import DataBase

router = Router()