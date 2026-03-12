from pathlib import Path
from src.db.database import DataBase
from src.config.conf_logs import logger

MIGRATIONS_DIR = Path(__file__).parent


def load_sql_files() -> list[str]:
    queries = []

    for file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        queries.append(file.read_text())

    return queries


async def run_migrations(db: DataBase) -> None:
    tables = load_sql_files()

    for query in tables:
        try:
            await db.executescript(query)
            logger.info(f"GOOD [✅]")

        except Exception:
            logger.error(f"FAIL [❌]", exc_info=True)
            raise