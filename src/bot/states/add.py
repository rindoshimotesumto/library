from aiogram.fsm.state import StatesGroup, State

class AddBook(StatesGroup):
    category_id = State()
    author_id = State()
    book_file_link = State()
    cover_file_id = State()
    book_name = State()
    description = State()
    year_of_publication = State()
    weight = State()
    language = State()
    rating = State()
    book_files_list = State()

class AddCategory(StatesGroup):
    c_id = State()
    c_name_upd = State()
    category_name = State()

class AddAuthor(StatesGroup):
    author_name = State()