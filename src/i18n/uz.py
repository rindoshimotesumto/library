# ==========================================
# Формат ключей: [модуль]:[сущность/раздел]:[действие/статус]
# ==========================================

UZ_TEXTS: dict[str, str] = {
    # --- Общие / Системные (common) ---
    "common:start": "📚 <b>Kitob botiga xush kelibsiz!</b>\nBu yerda siz turli kitoblarni topishingiz, o‘qishingiz va yuklab olishingiz mumkin.",
    "common:welcome_back": "👋 Yana ko‘rishganimizdan xursandmiz, <b>{name}</b>!",
    "common:choose_action": "Kerakli bo‘limni tanlang 👇",
    "common:loading": "⏳ Yuklanmoqda...",
    "common:pagination": "📄 Sahifa: {current}/{total}",

    # --- Ошибки и Статусы (error / success) ---
    "error:not_found": "❌ Ma'lumot topilmadi.",
    "error:access_denied": "⛔ Bu bo‘limga kirish uchun sizda ruxsat yo‘q.",
    "error:invalid_input": "⚠️ Noto‘g‘ri ma'lumot kiritildi. Iltimos, qaytadan urinib ko'ring.",
    "error:db_error": "❌ Tizimda xatolik yuz berdi. Keyinroq urinib ko'ring.",

    "success:saved": "✅ Muvaffaqiyatli saqlandi.",
    "success:deleted": "🗑 Muvaffaqiyatli o‘chirildi.",
    "success:updated": "✏️ Ma'lumotlar yangilandi.",

    # --- Раздел: Книги (book) ---
    "book:list_title": "📚 <b>Kitoblar ro‘yxati:</b>",
    "book:list_empty": "📭 Hozircha bu yerda kitoblar mavjud emas.",

    "book:info": (
        "📕 <b>Nomi:</b> {title}\n"
        "✍️ <b>Muallif:</b> {author}\n"
        "🗂 <b>Kategoriya:</b> {category}\n"
        "📄 <b>Hajmi:</b> {pages} bet\n"
        "🌐 <b>Tili:</b> {language}\n"
        "📅 <b>Nashr yili:</b> {year}\n"
        "⭐ <b>Reyting:</b> {rating}/5\n\n"
        "📝 <b>Tavsif:</b>\n<i>{description}</i>"
    ),

    # --- Раздел: Категории (category) ---
    "category:list_title": "🗂 <b>Kategoriyalar:</b>\nO‘zingizga yoqqan yo‘nalishni tanlang:",
    "category:empty": "📭 Kategoriyalar hali qo'shilmagan.",

    # --- Раздел: Поиск (search) ---
    "search:prompt": "🔎 Qidirmoqchi bo‘lgan kitobingiz yoki muallif nomini yozing:",
    "search:results": "🔎 <b>Qidiruv natijalari:</b>",
    "search:empty": "❌ Kechirasiz, so‘rovingiz bo‘yicha hech qanday kitob topilmadi.",

    # --- Раздел: Профиль пользователя (profile) ---
    "profile:info": (
        "👤 <b>Sizning profilingiz</b>\n\n"
        "🆔 <b>ID:</b> <code>{tg_id}</code>\n"
        "👤 <b>Ism:</b> {name}\n\n"
        "📊 <b>Sizning statistikangiz:</b>\n"
        "❤️ Yoqtirgan kitoblar: <b>{liked}</b> ta\n"
        "📖 O‘qilgan kitoblar: <b>{read}</b> ta\n"
        "⬇️ Yuklab olinganlar: <b>{downloaded}</b> ta"
    ),

    # --- Раздел: Добавление книги ---
    "admin:btn_add_book": "➕ Kitob qo‘shish",
    "admin:btn_my_books": "📚 Barcha kitoblar",

    "admin:prompt_book_name": "📝 Yangi kitob nomini kiriting:",
    "admin:prompt_book_desc": "📝 Kitob haqida qisqacha ma'lumot (tavsif) kiriting:",
    "admin:prompt_book_year": "📅 Nashr qilingan yilni kiriting (masalan, <i>1984</i>):",
    "admin:prompt_book_weight": "⚖️ Kitob varoq sonini kiriting (masalan, <i>350</i>):",
    "admin:prompt_book_lang": "🌐 Kitob tilini kiriting (masalan, <i>uz, ru, en</i>):",
    "admin:prompt_book_category": "📂 Ushbu kitob uchun kategoriyani tanlang:",
    "admin:prompt_book_author": "✍️ Kitob muallifini tanlang:",
    "admin:prompt_book_file": "📁 Kitob faylini (PDF/EPUB) (1ta) yuboring:",
    "admin:prompt_book_cover": "🖼 Endi kitob muqovasini (rasm) yuboring:",

    "admin:err_not_photo": "⚠️ Iltimos, hujjat (document) emas, oddiy rasm (photo) yuboring!",
    "admin:msg_cover_saved": "✅ Muqova qabul qilindi!",
    "admin:msg_book_added": "✅ <b>Kitob muvaffaqiyatli bazaga qo‘shildi!</b>",

    # --- Раздел: Категории (Categories) ---
    "admin:btn_categories": "📁 Kategoriyalar",
    "admin:btn_add_category": "➕ Kategoriya qo‘shish",
    "admin:prompt_category_name": "📝 Yangi kategoriya nomini kiriting:",
    "admin:msg_category_added": "✅ <b>Kategoriya muvaffaqiyatli qo‘shildi!</b>",

    # --- Раздел: Авторы (Authors) ---
    "admin:btn_authors": "✍️ Mualliflar",
    "admin:btn_add_author": "➕ Muallif qo‘shish",
    "admin:prompt_author_name": "📝 Muallifning ism-sharifini kiriting:",
    "admin:msg_author_added": "✅ <b>Muallif muvaffaqiyatli qo‘shildi!</b>",

    # --- Общие фразы (Errors & Navigation) ---
    "admin:btn_cancel": "❌ Bekor qilish",
    "admin:msg_canceled": "🚫 Amal bekor qilindi.",
    "admin:err_invalid_number": "⚠️ Iltimos, faqat raqam kiriting!",
}


UZ_BTNS: dict[str, dict[str, str]] = {

    # --- Главные меню ---
    "menu:main": {
        "menu:books": "📖 Kitoblar",
        "menu:categories": "🗂 Kategoriyalar",
        "menu:search": "🔎 Qidirish",
        "menu:profile": "👤 Profil",
        "menu:help": "❓ Yordam",
    },

    "menu:admin": {
        "admin:b:add": "➕ Kitob qo‘shish",
        "admin:b:del": "🗑 Kitob o‘chirish",
        "admin:c:add": "➕ Kategoriya qo‘shish",
        "admin:c:del": "🗑 Kategoriya o‘chirish",
        "admin:a:add": "➕ Muallif qo‘shish",
        "admin:a:del": "🗑 Muallif o'chirish",
    },

    # --- Навигация (Универсальная) ---
    "nav": {
        "nav:back": "⬅️ Orqaga",
        "nav:home": "🏠 Bosh sahifa",
        "nav:cancel": "❌ Bekor qilish",
        "nav:confirm": "✅ Tasdiqlash",
        "nav:prev": "⬅️ Oldingi",
        "nav:next": "Keyingi ➡️",
    },

    "book_actions": {
        "read": "📖 O‘qishni boshlash",
        "download": "⬇️ Yuklab olish",
        "like": "🤍 Yoqdi",
        "liked": "❤️ Yoqtirganlarda",
    }
}