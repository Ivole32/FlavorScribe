from config.config import (
    POSTGRES_URL,
    AUTO_MIGRATE_DATABASE_ON_STARTUP,
    DATABASE_BACKUP_ON_STARTUP,
    DATABASE_BACKUP_BEFORE_MIGRATION
)

from api.database.backup import backup_database
from api.database.migrate import migration_needed, run_alembic_upgrade_head

def startup_database():
    """
    Perform startup database checks and maintenance tasks.

    Actions performed:
    - Optionally create a backup
    - Run pending alembic migrations if enabled
    """
    needs_migration = migration_needed()

    # Backup database if database should be backuped at startup or a migration needs to be applied
    if DATABASE_BACKUP_ON_STARTUP or (needs_migration and DATABASE_BACKUP_BEFORE_MIGRATION and AUTO_MIGRATE_DATABASE_ON_STARTUP):
        backup_database(database_url=POSTGRES_URL)

    # migrate if migration is needed AND auto migrate is enabled
    if needs_migration and AUTO_MIGRATE_DATABASE_ON_STARTUP:
        run_alembic_upgrade_head()