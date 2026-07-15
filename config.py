"""Central configuration with environment variable overrides."""

from __future__ import annotations

import os


def _env_int(name: str, default: int) -> int:
    """Parse environment variable as int with fallback."""
    val = os.environ.get(name)
    if val is None:
        return default
    try:
        return int(val, 0)  # base=0 handles 0x prefix
    except ValueError:
        return default


def _env_str(name: str, default: str) -> str:
    """Get environment variable with fallback."""
    return os.environ.get(name, default)


def _env_bool(name: str, default: bool = False) -> bool:
    """Parse environment variable as boolean."""
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")


# Printer USB IDs
DEFAULT_VENDOR_ID = _env_int("PAPER_FEED_VENDOR_ID", 0x0483)
DEFAULT_PRODUCT_ID = _env_int("PAPER_FEED_PRODUCT_ID", 0x5840)

# Default feed modules
DEFAULT_OPTIONS = ["weather", "markets", "quote"]

# Market tickers for --markets (name -> yfinance symbol)
TICKERS = {
    "NIFTY": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK": "^NSEBANK",
    "N50": "NIFTYBEES.NS",
    "BANKB": "BANKBEES.NS",
    "IT": "ITBEES.NS",
    "PHARM": "PHARMABEES.NS",
    "AUTO": "AUTOBEES.NS",
    "CPSE": "CPSEETF.NS",
    "PSUB": "PSUBNKBEES.NS",
    "INFRA": "INFRABEES.NS",
    "GOLD": "GOLDBEES.NS",
    "HANG": "HNGSNGBEES.NS",
}

# RSS feed for news (can be overridden via PAPER_FEED_RSS_URL)
DEFAULT_RSS_URL = _env_str(
    "PAPER_FEED_RSS_URL",
    "https://www.thehindu.com/news/national/feeder/default.rss"
)

# Default weather city (can be overridden via PAPER_FEED_CITY)
DEFAULT_CITY = _env_str("PAPER_FEED_CITY", "Delhi")

# Enable debug logging (PAPER_FEED_DEBUG=1)
DEBUG = _env_bool("PAPER_FEED_DEBUG", False)