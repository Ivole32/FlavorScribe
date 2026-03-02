import os
from dotenv import load_dotenv
load_dotenv()

# General API information
API_TITLE = "FlavorScribe API"
API_DESCRIPTION = "The main API for FlavorScribe."
API_VERSION = "v1"
API_DOCS_ENABLED = True

# API rate Limit
API_RATE_LIMIT_ENABLED = True
API_DEFAULT_RATE_LIMITS = ["100/minute"]

# Auth Config
API_CLIENT_ID = os.getenv("CLIENT_ID", None)
API_CLIENT_SECRET = os.getenv("CLIENT_SECRET", None)
API_REDIRECT_URL = "http://localhost:8080/oauth/callback" 
API_AUTH_URL = "https://auth.hackclub.com/oauth/authorize"
API_TOKE_URL = "https://auth.hackclub.com/oauth/token"
API_API_ME = "https://auth.hackclub.com/api/v1/me"

# PostgreSQL configuration
POSTGRES_URL = os.getenv("DATABASE_URL", None)
POSTGRES_HOST = "127.0.0.1"
POSTGRES_PORT = 5432
POSTGRES_USER = os.getenv("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", None)
POSTGRES_MIN_CONNECTIONS = 1
POSTGRES_MAX_CONNECTIONS = 6
POSTGRES_CONNECT_TIMEOUT = 5.0
POSTGRES_RETRIES = 2
POSTGRES_RETRY_DELAY = 2.0
POSTGRES_HEALTHCHECK_TIMEOUT = 15.0
POSTGRES_HEALTHCHECK_INTERVALL = 5.0

# Database migration
ALEMBIC_INI_FILE = r"C:\Users\<hidden>\Documents\GitHub\falvorscribe\alembic.ini"
AUTO_MIGRATE_DATABASE_ON_STARTUP = True

# Database backup
DATABASE_BACKUP_DIR = r"C:\Users\<hidden>\Documents\GitHub\falvorscribe\backup"
DATABASE_BACKUP_BEFORE_MIGRATION = True
DATABASE_BACKUP_ON_STARTUP = False