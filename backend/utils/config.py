"""Configuration utilities for F1 Fantasy Analysis."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_DEBUG = os.getenv("API_DEBUG", "False").lower() in ("true", "1", "t")

# External API configuration
ERGAST_API_URL = os.getenv("ERGAST_API_URL", "https://ergast.com/api/f1")

# Database configuration (for future use)
DB_URL = os.getenv("DB_URL", "")

# Default fantasy settings
DEFAULT_BUDGET = float(os.getenv("DEFAULT_BUDGET", "100.0"))
MAX_DRIVERS = int(os.getenv("MAX_DRIVERS", "5"))

# Cache settings
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() in ("true", "1", "t")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour in seconds


def get_config() -> Dict[str, Any]:
    """Get the application configuration as a dictionary.

    Returns:
        Dictionary containing all configuration values
    """
    return {
        "api": {
            "host": API_HOST,
            "port": API_PORT,
            "debug": API_DEBUG,
        },
        "external_api": {
            "ergast_url": ERGAST_API_URL,
        },
        "database": {
            "url": DB_URL,
        },
        "fantasy": {
            "default_budget": DEFAULT_BUDGET,
            "max_drivers": MAX_DRIVERS,
        },
        "cache": {
            "enabled": CACHE_ENABLED,
            "ttl": CACHE_TTL,
        },
    } 