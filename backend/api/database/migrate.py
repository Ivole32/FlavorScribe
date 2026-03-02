import os
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv

from config.config import ALEMBIC_INI_FILE, POSTGRES_URL

from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine


def migration_needed() -> bool:
    """
    Check if database migration is needed.
    Returns:
        True: if migration is needed
        False: if migration is nt needed
    """

    if not POSTGRES_URL:
        raise RuntimeError("POSTGRES_URL not set")
    
    # Alembic config
    alembic_cfg = Config(ALEMBIC_INI_FILE)
    alembic_cfg.set_main_option("sqlalchemy.url", POSTGRES_URL)

    # Load script directory (migration files)
    script = ScriptDirectory.from_config(alembic_cfg)
    head_revision = script.get_current_head()

    # Connect to DB and get current revision
    engine = create_engine(POSTGRES_URL)
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        current_revision = context.get_current_revision()

    # If DB not at head -> migratioon needed
    return current_revision != head_revision

def run_alembic_upgrade_head():
    """
    Apply all pending Alembic migrations (upgrade to head)
    """
    # Check if alembic.ini exists
    if not os.path.exists(ALEMBIC_INI_FILE):
        raise FileNotFoundError(f"Alembic ini file not found {ALEMBIC_INI_FILE}")
    
    alembic_cfg = Config(ALEMBIC_INI_FILE)

    if POSTGRES_URL:
        alembic_cfg.set_main_option("sqlalchemy.url", POSTGRES_URL)

    # Set migration direction for logging
    os.environ["ALEMBIC_DIRECTION"] = "upgrade"

    # Migrate/Upgrade
    command.upgrade(alembic_cfg, "head")