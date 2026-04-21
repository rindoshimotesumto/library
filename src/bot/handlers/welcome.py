from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.command import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import main_menu

from src.db.database import DataBase
from src.db.repo.books import BookRepository
from src.db.repo.users import UsersRepository, User
from src.db.repo.stats import StatsRepository
from src.db.repo.authors import AuthorRepository
from src.db.repo.categories import CategoriesRepository

from src.config.conf_logs import logger

router = Router()
admin = {809673082}

async def check_user(message: Message | CallbackQuery, db: DataBase) -> str:
    user_repo = UsersRepository(db)
    have_u = await user_repo.get_user(message.from_user.id)

    if not have_u:
        if message.from_user.id not in admin:
            role = "user"
        else:
            role = "admin"

        await user_repo.add_user(message.from_user.id, role, "uz")
        return role

    return have_u.role

@router.message(CommandStart())
async def cmd_start(message: Message, state:FSMContext, db: DataBase):
    await state.clear()
    await check_user(message, db)
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
            logger.info(e)

    else:
        await message.answer(UZ_TEXTS["common:start"], reply_markup=await main_menu(True))

@router.message(Command("stats"))
async def cmd_stats(message: Message, state: FSMContext, db: DataBase):
    await state.clear()
    repo = StatsRepository(db)

    stats = await repo.stats("all")
    answer = (
        f"📚 Kitoblar: <code>{stats['b_count']}</code> ta\n"
        f"🗂 Kategoriyalar: <code>{stats['c_count']}</code> ta\n"
        f"✍️ Mualliflar: <code>{stats['a_count']}</code> ta\n"
        f"👥 Foydalanuvchilar: <code>{stats['u_count']}</code> ta"
    )

    await message.answer(answer)

@router.message(Command("change"))
async def cmd_stats(message: Message, state: FSMContext, db: DataBase):
    await state.clear()
    repo = BookRepository(db)

    if message.from_user.id not in admin:
        return

    await repo.change_link()

@router.message(Command("backup"))
async def backup(message: Message, state: FSMContext, db: DataBase):
    await state.clear()

    if message.from_user.id not in admin:
        try:
            if await check_user(message, db) != "admin":
                await message.answer(UZ_TEXTS["error:access_denied"])
                return

        except Exception as e:
            logger.info(e)

    try:
        backup_path = await db.backup()
        file = FSInputFile(backup_path)

        await message.answer_document(file, caption="Backup ✅")
        await db.clean_backups()
        return

    except Exception as e:
        await message.answer(f"Backup ⚠️: {str(e)}")
        return


@router.message(Command("rmc"))
async def remove_category(message: Message, command: CommandObject, db: DataBase):
    # 1. Проверяем, является ли пользователь админом
    users_repo = UsersRepository(db)
    user = await users_repo.get_user(message.from_user.id)

    if not user or user.role != "admin":
        # Если не админ, просто игнорируем команду (или можно отправить сообщение об отказе)
        return

    # 2. Проверяем, передал ли админ аргумент (ID категории)
    if not command.args:
        await message.answer("⚠️ Вы не указали ID категории.\nИспользование: `/rmc [id]`\nПример: `/rmc 5`",
                             parse_mode="Markdown")
        return

    # 3. Проверяем, является ли аргумент числом
    if not command.args.isdigit():
        await message.answer("⚠️ ID категории должен быть числом.")
        return

    category_id = int(command.args.replace(" ", ""))
    categories_repo = CategoriesRepository(db)

    # 4. Удаляем категорию
    deleted = await categories_repo.delete_category(category_id)

    if deleted:
        await message.answer(f"✅ Категория с ID {category_id} была успешно удалена.")
    else:
        await message.answer(f"❌ Категория с ID {category_id} не найдена.")


@router.message(Command("rma"))
async def remove_author(message: Message, command: CommandObject, db: DataBase):
    users_repo = UsersRepository(db)
    user = await users_repo.get_user(message.from_user.id)

    if not user or user.role != "admin":
        return

    if not command.args:
        await message.answer(
            "⚠️ Вы не указали ID автора.\nИспользование: `/rma [id]`\nПример: `/rma 7`",
            parse_mode="Markdown"
        )
        return

    if not command.args.isdigit():
        await message.answer("⚠️ ID автора должен быть числом.")
        return

    author_id = int(command.args)
    author_repo = AuthorRepository(db)

    try:
        await author_repo.delete_author(author_id)
        
        await message.answer(f"✅ Автор с ID {author_id} успешно удален (если он существовал).")
    except Exception as e:
        logger.error(f"Error deleting author: {e}")
        await message.answer(f"❌ Произошла ошибка при удалении автора.")

# @router.message(F.photo)
# async def cmd_photo(message: Message, db: DataBase):
#     await message.answer(message.photo[-1].file_id)
#
# @router.message(F.document)
# async def cmd_document(message: Message, db: DataBase):
#     await message.answer(message.document.file_id)
