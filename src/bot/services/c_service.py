# from src.config.logs_conf import logger
from src.data.database import Database
from src.data.repo.categories import Category, AddCategory, EditCategory, DeleteCategory

async def cmd_new_category_service(c_name: str, db: Database) -> str:
    result = await AddCategory(db).add_category(c_name)

    if result == -1:
        return f"Category {c_name} already exists."

    return f"Category {c_name} #{result} has been added."

async def cmd_edit_category_service(old_c_name: str, new_c_name: str, db: Database) -> str:
    c_id = await Category(db).search_category(old_c_name)
    result = await EditCategory(db).edit_category(c_id, new_c_name)

    if result in (-1, -2):
        return f"Category {old_c_name} #{result} can't be edited."

    return f"Category {old_c_name} -> {result} has been edited."

async def cmd_delete_category_service(category_name: str, db: Database) -> str:
     result = await DeleteCategory(db).delete_category(category_name)

     if result in (-1, -2):
         return f"Category {category_name} #{result} can't be deleted."

     return f"Category {category_name} #{result} has been deleted."