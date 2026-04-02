from pathlib import Path
from src.data.database import Database
from src.config.logs_conf import logger

MIGRATIONS_DIR = Path(__file__).parent

def load_sql_files() -> dict[str, str]:
    queries = {}

    for file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        queries[file.name] = file.read_text()

    return queries

async def run_migrations(db: Database) -> None:
    tables = load_sql_files()

    for name, query in tables.items():
        try:
            await db.execute(query)
            logger.info(f"{name} [CREATED]")

        except Exception:
            logger.error(f"{name} [X]", exc_info=True)
            raise