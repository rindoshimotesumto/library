from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def next_state() -> ReplyKeyboardMarkup:
    # Создаем кнопку
    button = KeyboardButton(text="Keyingisi ➡️")

    # Создаем клавиатуру
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [button]  # Кнопка в первом ряду
        ],
        resize_keyboard=True,  # Чтобы кнопка была компактной, а не на пол-экрана
        one_time_keyboard=True  # Исчезнет после одного нажатия
    )

    return markup