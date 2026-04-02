from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command, CommandObject

from redis.asyncio import Redis

# from src.config.logs_conf import logger

from src.i18n.i18n import DEFAULT_LANG

from src.data.database import Database
from src.i18n.i18n import t, langs_
from src.bot.keyboards.inline import menu
from src.bot.services.cache_service import UserCacheService

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, redis: Redis):
    user_service = UserCacheService(redis)
    user_id = message.from_user.id
    is_user = await user_service.get_user(user_id)
    default_data = user_service.default_data

    if not is_user:
        await user_service.update_user(user_id, **default_data)
        is_user = default_data

    lang = is_user.get('lang', 'uz')
    answer = t("start", lang)

    kb = await menu(lang)
    await message.answer(answer, reply_markup=kb)


@router.message(Command('lang'))
async def cmd_lang(message: Message, command: CommandObject, redis: Redis, db: Database):
    if message.chat.type != 'private':
        return

    user_service = UserCacheService(redis)
    default_data = user_service.default_data
    user_lang = await user_service.get_user(message.from_user.id)

    if command.args is not None:
        lang = command.args.replace(" ", "")

        if lang in langs_:
            user_id = message.from_user.id

            kwargs_ = {
                'lang': lang
            }

            await user_service.update_user(user_id, **kwargs_)
            answer = t("lang:changed", lang)

        else:
            answer = t("lang:another", user_lang.get('lang', default_data.get('lang')))

    else:
        answer = t("lang:another", user_lang.get('lang', default_data.get('lang')))

    await message.answer(answer)