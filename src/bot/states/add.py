from aiogram.fsm.state import StatesGroup, State

class AddBook(StatesGroup):
    category_id = State()
    author_id = State()
    cover_file_id = State()
    book_name = State()
    description = State()
    year_of_publication = State()
    weight = State()
    language = State()
    rating = State()
    book_file = State()

class AddCategory(StatesGroup):
    category_name = State()

class AddAuthor(StatesGroup):
    author_name = State()