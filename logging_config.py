# logging_config.py

# Imports
import logging
from logging.handlers import RotatingFileHandler
import os

# Logging configuration
LOG_DIR = "logs" # Directory in current path to store log files
LOG_FILE = os.path.join(LOG_DIR, "app.log") # Log file path and name
MAX_LOG_SIZE = 200 * 1024 * 1024  # 200 MB
BACKUP_COUNT = 3 # Number of backup log files to keep (Rotating files ones max size is reached)

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) # Log level set to DEBUG to capture all levels

    # Log message format with timestamp, log level, filename, line number and message
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)
