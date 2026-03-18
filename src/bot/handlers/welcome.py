from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import main_menu

from src.db.database import DataBase
from src.db.repo.users import UsersRepository, User

from src.config.conf_logs import logger

router = Router()
admin = set()

async def check_user(message: Message, db: DataBase) -> str:
    user_repo = UsersRepository(db)
    have_u = await user_repo.get_user(message.from_user.id)

    if not have_u:
        await user_repo.add_user(message.from_user.id, "user", "uz")

    return have_u.role

@router.message(CommandStart())
async def cmd_start(message: Message, state:FSMContext, db: DataBase):
    await state.clear()
    await message.answer(UZ_TEXTS["common:start"], reply_markup=await main_menu(False))

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext, db: DataBase):
    await state.clear()

    if message.from_user.id not in admin:
        try:
            if await check_user(message, db) == "admin":
                await message.answer(UZ_TEXTS["common:start"], reply_markup=await main_menu(True))
                admin.add(message.from_user.id)

            else:
                await message.answer(UZ_TEXTS["error:access_denied"])

        except Exception as e:
            logger.info(str(e))

    else:
        await message.answer(UZ_TEXTS["common:start"], reply_markup=await main_menu(True))

@router.message(Command("backup"))
async def backup(message: Message, state: FSMContext, db: DataBase):
    await state.clear()

    if message.from_user.id not in admin:
        try:
            if await check_user(message, db) == "admin":

                try:
                    backup_path = await db.backup()
                    await db.clean_backups()
                    file = FSInputFile(backup_path)

                    await message.answer(text="Backup ✅")
                    return

                except Exception as e:
                    await message.answer(f"Backup ⚠️: {str(e)}")
                    return

            else:
                await message.answer(UZ_TEXTS["error:access_denied"])
                return

        except Exception as e:
            logger.info(str(e))

    await message.answer(UZ_TEXTS["error:access_denied"])

# @router.message(F.photo)
# async def cmd_photo(message: Message, db: DataBase):
#     await message.answer(message.photo[-1].file_id)
#
# @router.message(F.document)
# async def cmd_document(message: Message, db: DataBase):
#     await message.answer(message.document.file_id)