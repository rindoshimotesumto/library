from aiogram.fsm.state import State, StatesGroup

class AddBookState(StatesGroup):
    book_name = State()
    book_date = State()
    book_author = State()
    book_category = State()
    book_description = State()
    book_pages = State()
    book_language = State()
