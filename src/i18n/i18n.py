from enum import Enum
from src.config.logs_conf import logger

class Langs(str, Enum):
    uz = "uz"
    ru = "ru"
    en = "en"

langs_ = [lang.value for lang in Langs]
DEFAULT_LANG = Langs.uz

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
        "uz": "🔎 Kitob qidirish",
        "ru": "🔎 Поиск книги",
        "en": "🔎 Search for a book"
    },
    "search:author": {
        "uz": "👤 Muallif qidirish",
        "ru": "👤 Поиск автора",
        "en": "👤 Search for an author"
    },
    "profile": {
        "uz": "👤 Profil ma’lumotlari",
        "ru": "👤 Информация профиля",
        "en": "👤 Profile information",
    },
    "random:books": {
        "uz": "🎲 Tasodifiy kitoblar",
        "ru": "🎲 Случайные книги",
        "en": "🎲 Random books"
    },
    "settings": {
        "uz": "⚙️ Sozlamalar",
        "ru": "⚙️ Настройки",
        "en": "⚙️ Settings",
    },
    "no:books": {
        "uz": "📭 Bu kategoriyada kitoblar yo‘q",
        "ru": "📭 В этой категории нет книг",
        "en": "📭 No books in this category",
    },
    "not:subscribe": {
        "uz": (
            "❌ Botdan foydalanish uchun kanalga obuna bo‘lishingiz kerak.\n\n"
            "📢 Iltimos, quyidagi kanalga obuna bo‘ling va \"Tekshirish\" tugmasini bosing."
        ),
        "ru": (
            "❌ Для использования бота необходимо подписаться на канал.\n\n"
            "📢 Пожалуйста, подпишитесь на канал ниже и нажмите кнопку «Проверить»."
        ),
        "en": (
            "❌ To use this bot, you need to subscribe to the channel.\n\n"
            "📢 Please subscribe to the channel below and press the \"Check\" button."
        )
    },
    "not:subscribe:show_alert": {
        "uz": "Obunasiz davom etish mumkin emas.",
        "ru": "Невозможно продолжить — вы не подписаны.",
        "en": "Cannot continue — you are not subscribed."
    },
    "check:subscribe": {
        "uz": "✅ Tekshirish",
        "ru": "✅ Проверить",
        "en": "✅ Check",
    },
    "favorite:books": {
        "uz": "❤️‍🔥 Sevimli",
        "ru": "❤️‍🔥 Избранные",
        "en": "❤️‍🔥 Favorites"
    },
    "choose:category": {
        "uz": "🗂 Kitob kategoriyasini tanlang",
        "ru": "🗂 Выберите категорию книги",
        "en": "🗂 Choose a book category"
    },
    "choose:collection": {
        "uz": "🗂 Kitoblar to‘plamini tanlang",
        "ru": "🗂 Выберите коллекцию книг",
        "en": "🗂 Choose a book collection"
    },
    "add:cover": {
        "uz": "📷 Muqova rasmini yuboring",
        "ru": "📷 Отправьте обложку книги",
        "en": "📷 Send the book cover"
    },
    "add:category": {
        "uz": "📂 Kategoriyani tanlang",
        "ru": "📂 Выберите категорию",
        "en": "📂 Select category"
    },
    "add:collection": {
        "uz": "🗂 To‘plamni tanlang",
        "ru": "🗂 Выберите коллекцию",
        "en": "🗂 Select collection"
    },
    "add:title": {
        "uz": "✏️ Kitob nomini kiriting",
        "ru": "✏️ Введите название книги",
        "en": "✏️ Enter book title"
    },
    "add:author": {
        "uz": "👤 Muallifni tanlang",
        "ru": "👤 Выберите автора",
        "en": "👤 Select author"
    },
    "add:description": {
        "uz": "📝 Kitob tavsifini kiriting",
        "ru": "📝 Введите описание книги",
        "en": "📝 Enter book description"
    },
    "add:language": {
        "uz": "🌐 Kitob tilini tanlang",
        "ru": "🌐 Выберите язык книги",
        "en": "🌐 Select book language"
    },
    "add:year_of_publication": {
        "uz": "📅 Nashr yilini kiriting",
        "ru": "📅 Укажите год издания",
        "en": "📅 Enter publication year"
    },
    "add:number_of_pages": {
        "uz": "📖 Sahifalar sonini kiriting",
        "ru": "📖 Укажите количество страниц",
        "en": "📖 Enter number of pages"
    },
    "add:weight": {
        "uz": "⚖️ Kitob og‘irligini kiriting (gramm)",
        "ru": "⚖️ Укажите вес книги (в граммах)",
        "en": "⚖️ Enter book weight (grams)"
    },
    "add:next_part": {
        "uz": "➡️ Keyingi qismni tanlang (agar mavjud bo‘lsa)",
        "ru": "➡️ Выберите следующую часть (если есть)",
        "en": "➡️ Select next part (if any)"
    },
    "add:link": {
        "uz": "🔗 Yuklab olish havolasini yuboring",
        "ru": "🔗 Отправьте ссылку для скачивания",
        "en": "🔗 Send download link"
    },
    "cover:invalid": {
        "uz": "❌ Rasm yuboring (faqat foto).",
        "ru": "❌ Отправьте изображение (только фото).",
        "en": "❌ Please send an image (photo only)."
    },
    "category:invalid": {
        "uz": "❌ Noto‘g‘ri kategoriya.",
        "ru": "❌ Некорректная категория.",
        "en": "❌ Invalid category."
    },
    "collection:invalid": {
        "uz": "❌ Noto‘g‘ri to‘plam.",
        "ru": "❌ Некорректная коллекция.",
        "en": "❌ Invalid collection."
    },
    "title:invalid": {
        "uz": "❌ Kitob nomi faqat harflardan iborat bo‘lishi kerak.",
        "ru": "❌ Название должно состоять только из букв.",
        "en": "❌ Title must contain letters only."
    },
    "author:invalid": {
        "uz": "❌ Noto‘g‘ri muallif.",
        "ru": "❌ Некорректный автор.",
        "en": "❌ Invalid author."
    },
    "description:invalid": {
        "uz": "❌ Tavsif juda qisqa.",
        "ru": "❌ Описание слишком короткое.",
        "en": "❌ Description is too short."
    },
    "language:invalid": {
        "uz": "❌ Noto‘g‘ri til.",
        "ru": "❌ Некорректный язык.",
        "en": "❌ Invalid language."
    },
    "year_of_publication:invalid": {
        "uz": "❌ To‘g‘ri yil kiriting (masalan: 2022).",
        "ru": "❌ Укажите корректный год (например: 2022).",
        "en": "❌ Enter a valid year (e.g. 2022)."
    },
    "number_of_pages:invalid": {
        "uz": "❌ Sahifalar soni raqam bo‘lishi kerak.",
        "ru": "❌ Количество страниц должно быть числом.",
        "en": "❌ Pages must be a number."
    },
    "weight:invalid": {
        "uz": "❌ Og‘irlik raqamda bo‘lishi kerak (gramm).",
        "ru": "❌ Вес должен быть числом (в граммах).",
        "en": "❌ Weight must be a number (grams)."
    },
    "next_part:invalid": {
        "uz": "❌ Noto‘g‘ri qism tanlandi.",
        "ru": "❌ Некорректная часть.",
        "en": "❌ Invalid next part."
    },
    "link:invalid": {
        "uz": "❌ Noto‘g‘ri havola.",
        "ru": "❌ Некорректная ссылка.",
        "en": "❌ Invalid link."
    }
}

MAIN_MSG_BTNS = ["search:book", "search:author", "random:books", "favorite:books"]
CHECK_SUBSCRIBE_BTN = "check:subscribe"

def t(key: str, lang: str | Langs = None, **kwargs) -> str:
    if isinstance(lang, Langs):
        lang_code = lang.value
    else:
        lang_code = (lang or DEFAULT_LANG.value).lower()

    translations = I18N.get(key)
    if not translations:
        return key

    text = translations.get(lang_code)

    if not text:
        text = translations.get(DEFAULT_LANG.value) or next(iter(translations.values()), key)

    try:
        return text.format(**kwargs)
    except (KeyError, ValueError) as e:
        logger.error("'%s' (args: %s): %s", key, kwargs, e)
        return text