from enum import Enum
from src.config.logs_conf import logger

class Langs(Enum):
    uz = "uz"
    ru = "ru"
    en = "en"

langs_ = [lang.value for lang in Langs]
DEFAULT_LANG = Langs.uz.value

I18N = {
    "start": {
        "uz": "📚 Kutubxonaga xush kelibsiz",
        "ru": "📚 Добро пожаловать в библиотеку",
        "en": "📚 Welcome to the library",
    },
    "language:select": {
        "uz": "🌐 Tilni tanlang",
        "ru": "🌐 Выберите язык",
        "en": "🌐 Choose language",
    },
    "lang:changed": {
        "uz": "✅ Til o'zgartirildi",
        "ru": "✅ Язык изменен",
        "en": "✅ Lang changed"
    },
    "lang:fail": {
        "uz": "❌ Til o‘zgartirilmadi",
        "ru": "❌ Язык не изменился",
        "en": "❌ Language was not changed"
    },
    "lang:another": {
        "uz": "🙏 Iltimos, to'g'ri tilni tanlang (O'zbekcha / Русский / English)",
        "ru": "🙏 Пожалуйста, выберите правильный язык (O'zbekcha / Русский / English)",
        "en": "🙏 Please choose the correct language (O'zbekcha / Русский / English)"
    },
    "menu": {
        "uz": "📖 Asosiy menyu",
        "ru": "📖 Главное меню",
        "en": "📖 Main menu",
    },
    "categories": {
        "uz": "📂 Kategoriyalar",
        "ru": "📂 Категории",
        "en": "📂 Categories",
    },
    "audio_books": {
        "uz": "📚 Audio kitoblar",
        "ru": "📚 Аудио книги",
        "en": "📚 Audio books",
    },
    "search:book": {
        "uz": "🔎 Kitob nomini kiriting",
        "ru": "🔎 Введите название книги",
        "en": "🔎 Enter book title",
    },
    "profile": {
        "uz": "👤 Profil ma’lumotlari",
        "ru": "👤 Информация профиля",
        "en": "👤 Profile information",
    },
    "settings": {
        "uz": "⚙️ Sozlamalar",
        "ru": "⚙️ Настройки",
        "en": "⚙️ Settings",
    },
    "no_books": {
        "uz": "📭 Bu kategoriyada kitoblar yo‘q",
        "ru": "📭 В этой категории нет книг",
        "en": "📭 No books in this category",
    }
}

MAIN_MSG_BTNS = ["categories", "audio_books", "search:book"]

def t(key: str, lang: str | Langs = None, **kwargs) -> str:
    if isinstance(lang, Langs):
        lang_code = lang.value
    else:
        lang_code = (lang or DEFAULT_LANG).lower()

    translations = I18N.get(key)
    if not translations:
        return key

    text = translations.get(lang_code)

    if not text:
        text = translations.get(DEFAULT_LANG) or next(iter(translations.values()), key)

    try:
        return text.format(**kwargs)
    except (KeyError, ValueError) as e:
        logger.error("'%s' (args: %s): %s", key, kwargs, e)
        return text