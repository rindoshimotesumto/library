UZ_TEXTS: dict[str, str] = {
    # ===== Main =====
    "start": "📚 Kitob botiga xush kelibsiz!\nBu yerda siz turli kitoblarni topishingiz va o‘qishingiz mumkin.",
    "welcome:back": "👋 Yana ko‘rishganimizdan xursandmiz!",
    "choose:action": "Kerakli bo‘limni tanlang 👇",

    # ===== Books =====
    "books:list": "📚 Kitoblar ro‘yxati",
    "no:books": "Hozircha kitoblar mavjud emas.",
    "book:overview": "📖 Kitob haqida",
    "book:title": "📕 Nomi",
    "book:author": "✍️ Muallif",
    "book:description": "📝 Tavsif",
    "book:pages": "📄 Sahifalar soni",
    "book:language": "🌐 Til",
    "book:year": "📅 Nashr yili",
    "book:rating": "⭐ Reyting",
    "book:read": "📖 O‘qishni boshlash",
    "book:download": "⬇️ Yuklab olish",

    # ===== Search =====
    "search:prompt": "🔎 Kitob nomini yozing:",
    "searching": "🔍 Qidirilmoqda...",
    "no:search": "🔍 Hozircha qidiruv uchun, kitoblar mavjud emas.",
    "search:no:results": "❌ Hech qanday natija topilmadi.",
    "search:results": "🔎 Qidiruv natijalari",

    # ===== Profile =====
    "profile": "👤 Sizning profilingiz",
    "no:profile": "👤 Profil mavjud emas.",
    "profile:id": "🆔 ID",
    "profile:name": "👤 Ism",
    "profile:joined": "📅 Qo‘shilgan sana",
    "profile:books:read": "📚 O‘qilgan kitoblar",

    # ===== Categories =====
    "categories": "📚 Kategoriyalar",
    "no:categories": "Hozircha kategoriyalar mavjud emas.",
    "category:choose": "Kategoriyani tanlang",

    # ===== Help =====
    "help": (
        "❓ Yordam\n\n"
        "Bu bot orqali siz:\n"
        "• kitoblarni ko‘rishingiz\n"
        "• kitoblarni qidirishingiz\n"
        "• kitoblarni o‘qishingiz yoki yuklab olishingiz mumkin."
    ),

    # ===== Errors =====
    "error": "❌ Xatolik yuz berdi.",
    "not:found": "❌ Ma'lumot topilmadi.",
    "access:denied": "⛔ Sizda ruxsat yo‘q.",
    "invalid:input": "⚠️ Noto‘g‘ri ma'lumot kiritildi.",

    # ===== System =====
    "loading": "⏳ Yuklanmoqda...",
    "success": "✅ Amal muvaffaqiyatli bajarildi.",
    "saved": "💾 Saqlandi.",
    "deleted": "🗑 O‘chirildi.",
    "updated": "✏️ Yangilandi.",

    # ===== Pagination =====
    "page": "📄 Sahifa",
    "of": "dan",

    # ===== Confirmation =====
    "are_you_sure": "Haqiqatan ham davom etmoqchimisiz?",
    "yes": "Ha",
    "no": "Yo‘q",
    
    "admin:panel": "🛠 Admin panel",
    "no:settings": "Sozlanmoqda!"
}


UZ_BTNS: dict[str, dict[str, str]] = {
    "main_menu": {
        # ===== Menu =====
        "menu:books": "📖 Kitoblar",
        "menu:categories": "📚 Kategoriyalar",
        "menu:search": "🔎 Qidirish",
        "menu:profile": "👤 Profil",
        "menu:help": "❓ Yordam",
        "menu:settings": "⚙️ Sozlamalar"
    },

    # ===== Navigation =====
    "navigation_menu": {
        "back": "⬅️ Orqaga",
        "next": "➡️ Keyingi",
        "previous": "⬅️ Oldingi",
        "home": "🏠 Bosh sahifa",
        "cancel": "❌ Bekor qilish",
        "confirm": "✅ Tasdiqlash"
    },
    
    "admin_panel": {
        # ===== Admin Panel =====
        "admin:add:book": "➕ Kitob qo‘shish",
        "admin:delete:book": "🗑 Kitob o‘chirish",
        "admin:edit:book": "✏️ Kitobni tahrirlash",
        "admin:add:category": "➕ Kategoriya qo‘shish",
        "admin:delete:category": "🗑 Kategoriya o‘chirish",
        "admin:edit:category": "✏️ Kategoriya tahrirlash",
    },
}