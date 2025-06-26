import os
import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    root_dir = Path(sys.executable).parent.parent.absolute()
else:
    root_dir = Path(__file__).parent.parent.absolute()

TESTS_DIR: str = os.path.join(root_dir, "tests")
MOCKS_DIR: str = os.path.join(root_dir, "mocks")

ADMIN_DIR: str = os.path.join(root_dir, "admin")
BOT_DIR: str = os.path.join(root_dir, 'bot')

TEMPLATES_DIR: str = os.path.join(ADMIN_DIR, "templates")
STATIC_DIR: str = os.path.join(ADMIN_DIR, "static")

MOCK_DB_PATH: str = os.path.join(MOCKS_DIR, "mock_db.json")

BOT_LOGS_DIR: str = os.path.join(BOT_DIR, "logs")
BOT_LOGS_PATH: str = os.path.join(BOT_LOGS_DIR, "logs.txt")

ADMIN_LOGS_DIR: str = os.path.join(ADMIN_DIR, "logs")
ADMIN_LOGS_PATH: str = os.path.join(ADMIN_LOGS_DIR, "logs.txt")

CLAIM_LINKS: dict[str, str] = {
    "sophon": "https://claim.sophon.xyz/",
    "sxt": "https://gigaclaim.spaceandtime.io/",
    "og": "https://claim.0gfoundation.ai/unlock",
    "jager": "https://jager.meme/",
}

FORMATTED_NAMES: dict[str, str] = {
    "sophon": "Sophon",
    "sxt": "Space and Time",
    "og": "0G",
    "jager": "Jager (BNB memecoin)",
}

TICKERS: dict[str, str] = {
    "sophon": "$SOPH",
    "sxt": "$SXT",
    "og": "$OG",
    "jager": "$JAGER",
}

ALL_PROJECTS: list[str] = ["sophon", "sxt", "og", "jager"]

TOKENS_PER_NODE_0G: int = 1143

MAX_INT64: int = 9223372036854775807

PAGE_SIZE: int = 5
BATCH_SIZE: int = 20

FULL_RESULTS_TEMP_CSV: str = "temp_full_results.csv"
FULL_RESULTS_CSV: str = "full_results.csv"
ELIGIBLE_RESULTS_TEMP_CSV: str = "temp_eligible_results.csv"
ELIGIBLE_RESULTS_CSV: str = "eligible_results.csv"

BOT_CONTAINER_NAME: str = "telegram-bot"
