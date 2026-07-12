# Test configuration and fixtures
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_printer():
    """Create a mock printer object."""
    printer = MagicMock()
    printer.text = MagicMock()
    printer.set = MagicMock()
    printer.image = MagicMock()
    printer.ln = MagicMock()
    return printer


@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing."""
    return {
        "description": "Partly cloudy",
        "temp": "25",
        "feels_like": "27",
        "humidity": "65",
        "chance_of_rain": "20",
        "precip": "0.0",
        "sunrise": "06:15",
        "sunset": "18:30",
        "moon_phase": "Waxing Gibbous",
        "moon_illumination": "65",
    }


@pytest.fixture
def sample_quote_data():
    """Sample quote data for testing."""
    return {
        "content": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
    }


@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    return {
        "week": 2.5,
        "month": -1.2,
        "year": 15.8,
    }


@pytest.fixture
def sample_financials():
    """Sample financial data for testing."""
    return {
        "market_cap": 2800000000000,
        "pe_ratio": 28.5,
        "dividend_yield": 0.005,
        "high_52wk": 198.23,
        "low_52wk": 124.17,
    }