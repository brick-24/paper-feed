"""Shared test fixtures and configuration."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock heavy dependencies at module level
sys.modules["yfinance"] = MagicMock()
sys.modules["numpy"] = MagicMock()
sys.modules["pandas"] = MagicMock()


class MockFeedParser:
    """Mock feedparser.parse return value."""

    def __init__(self, entries):
        self.entries = entries


@pytest.fixture
def mock_printer():
    """Create a mock printer with commonly used methods."""
    printer = MagicMock()
    printer.set = MagicMock()
    printer.text = MagicMock()
    printer.ln = MagicMock()
    printer.image = MagicMock()
    return printer


@pytest.fixture
def sample_rss_feed():
    """Sample RSS feed data for testing."""
    return {
        "entries": [
            {"title": "Breaking News: Test Headline One"},
            {"title": "Another Important Story Here"},
            {"title": "Third News Item With Longer Title That Should Be Truncated"},
        ]
    }


@pytest.fixture
def sample_forecast_data():
    """Sample forecast API response."""
    return {
        "daily": {
            "time": ["2026-07-14", "2026-07-15", "2026-07-16"],
            "weathercode": [0, 1, 61],
            "temperature_2m_max": [32.5, 31.0, 28.5],
            "temperature_2m_min": [24.0, 23.5, 22.0],
            "precipitation_probability_max": [0, 10, 80],
        }
    }


@pytest.fixture
def sample_xkcd_data():
    """Sample XKCD API response."""
    return {
        "num": 2950,
        "safe_title": "Test Comic",
        "img": "https://imgs.xkcd.com/comics/test.png",
    }


@pytest.fixture
def temp_image_file(tmp_path):
    """Create a temporary image file for testing."""
    img_file = tmp_path / "test_image.png"
    img_file.write_bytes(b"fake image data")
    return img_file