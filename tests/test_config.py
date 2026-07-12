"""Tests for config module."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import config


def test_default_vendor_and_product_ids():
    """Test default vendor and product IDs are set correctly."""
    assert config.DEFAULT_VENDOR_ID == 0x0483
    assert config.DEFAULT_PRODUCT_ID == 0x5840


def test_default_options():
    """Test default options list."""
    assert config.DEFAULT_OPTIONS == ["weather", "markets", "quote"]


def test_tickers_dict_structure():
    """Test TICKERS dictionary has expected structure."""
    assert isinstance(config.TICKERS, dict)
    assert "NIFTY" in config.TICKERS
    assert "SENSX" in config.TICKERS
    assert config.TICKERS["NIFTY"] == "^NSEI"
    assert config.TICKERS["SENSX"] == "^BSESN"


def test_all_tickers_are_strings():
    """Test all ticker values are strings."""
    for name, symbol in config.TICKERS.items():
        assert isinstance(name, str)
        assert isinstance(symbol, str)
        assert len(symbol) > 0