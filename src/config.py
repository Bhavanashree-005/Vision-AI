"""Configuration and constants for the AI Code Assistant."""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
HISTORY_FILE = DATA_DIR / "chat_history.json"
ENV_FILE = BASE_DIR / ".env"

# --- Ensure directories exist ---
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Load .env file ---
load_dotenv(ENV_FILE)

# --- Logging setup ---
LOG_FILE = LOGS_DIR / "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("ai_code_assistant")

# --- API Configuration ---
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash"
SITE_URL = "https://github.com/yourusername/visioncode-ai"
SITE_NAME = "VisionCode AI"

# --- Timeouts ---
REQUEST_TIMEOUT = 30  # seconds


def get_api_key() -> Optional[str]:
    """Retrieve the OpenRouter API key from environment or .env file."""
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key.strip()
    return None


def set_api_key(key: str) -> None:
    """Persist API key to .env file."""
    try:
        with open(ENV_FILE, "a", encoding="utf-8") as f:
            f.write(f"\nOPENROUTER_API_KEY={key.strip()}\n")
        os.environ["OPENROUTER_API_KEY"] = key.strip()
        logger.info("API key saved to .env file.")
    except OSError as exc:
        logger.error("Failed to save API key: %s", exc)