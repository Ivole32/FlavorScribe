# Logging core
import logging
from logging.handlers import RotatingFileHandler

# Path utility
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

LOG_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

# Create and configure logger
def setup_logger() -> logging.Logger:
    logger = logging.getLogger("app")
    logger.setLevel(LOG_LEVEL)

    # Prevents adding multiple handlers if called multiple times
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(LOG_FORMAT)

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler with totation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8"
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

def log(level: int, message: str) -> None:
    logger.log(level, message)