from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command, CommandObject

from src.i18n.i18n import t, Langs
from src.bot.services.cache_service import DefaultUserData, UserCacheService
from src.data.repo.user import UserRepo
from src.bot.keyboards.inline import menu_kb

from src.config.logs_conf import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, user: DefaultUserData):
    answer = t('start', user.lang)
    kb = await menu_kb(user.lang)

    await message.answer(answer, reply_markup=kb)

@router.message(Command('lang'))
async def change_lang(
        message: Message,
        command: CommandObject,
        user: DefaultUserData,
        user_cache: UserCacheService,
        user_repo: UserRepo
):
    lang = command.args.replace(" ", "").lower()

    try:
        lang = Langs(lang)
        user.lang = lang.value

        await user_cache.update_user(message.from_user.id, **dict(user))
        await user_repo.update_lang(message.from_user.id, lang)
        answer = t('lang:changed', user.lang)

    except Exception as e:
        logger.exception(f"lang error: {user.tg_id} - {lang}")
        answer = t('lang:another', user.lang)

    await message.answer(answer)