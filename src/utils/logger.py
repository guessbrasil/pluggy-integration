from loguru import logger
import sys
import os
from src.config.settings import LOG_LEVEL

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()

# Log no terminal
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    level=LOG_LEVEL
)

# Log geral
logger.add(
    f"{LOG_DIR}/app.log",
    rotation="10MB",
    retention="7 days",
    level=LOG_LEVEL
)

# Logs específicos com filtros baseados na mensagem
logger.add(
    f"{LOG_DIR}/items.log",
    rotation="10 MB",
    retention="7 days",
    level=LOG_LEVEL,
    filter=lambda record: record["message"].startswith("ITEMS")
)

logger.add(
    f"{LOG_DIR}/accounts.log",
    rotation="10 MB",
    retention="7 days",
    level=LOG_LEVEL,
    filter=lambda record: record["message"].startswith("ACCOUNTS")
)

logger.add(
    f"{LOG_DIR}/transactions.log",
    rotation="10 MB",
    retention="7 days",
    level=LOG_LEVEL,
    filter=lambda record: record["message"].startswith("TRANSACTIONS")
)
