"""Application settings and environment variable access."""

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

APP_NAME = "Lumière"
TAGLINE = "Where curiosity meets elegance"
DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_TEMPERATURE = 0.7
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 1.5
TEMPERATURE_STEP = 0.05
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def get_openrouter_api_key() -> str | None:
	"""Return the configured OpenRouter key, or ``None`` when unset."""
	api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
	return api_key or None
