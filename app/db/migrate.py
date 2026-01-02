from alembic import command
from alembic.config import Config
import os
import logging

logger = logging.getLogger(__name__)

def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")

        db_url = os.getenv("DATABASE_URL")
        if db_url:
            alembic_cfg.set_main_option("sqlalchemy.url", db_url)

        command.upgrade(alembic_cfg, "head")
        logger.info("Alembic migrations applied successfully")

    except Exception as e:
        # 🔥 NUNCA derruba o app no Render
        logger.error(f"Alembic migration failed: {e}")
