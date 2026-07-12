"""Tests for stock module."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock yfinance before importing stock
with patch.dict("sys.modules", {"yfinance": MagicMock()}):
    from function.stock import calculate_returns, format_market_cap, get_financials, print_stock


class TestCalculateReturns:
    """Tests for calculate_returns function."""

    def test_calculate_returns_insufficient_history(self):
        """Test calculate_returns with insufficient history."""
        mock_ticker = MagicMock()
        mock_hist = MagicMock()
        mock_closes = MagicMock()
        mock_dropped = MagicMock()
        mock_dropped.__len__ = MagicMock(return_value=10)
        mock_closes.dropna.return_value = mock_dropped
        mock_hist.__getitem__.return_value = mock_closes
        mock_ticker.history.return_value = mock_hist

        with patch("function.stock.yf.Ticker", return_value=mock_ticker):
            with pytest.raises(ValueError, match="Not enough history"):
                calculate_returns("AAPL")


class TestFormatMarketCap:
    """Tests for format_market_cap function."""

    def test_format_market_cap_none(self):
        """Test format_market_cap with None value."""
        assert format_market_cap(None) == "N/A"

    def test_format_market_cap_small(self):
        """Test format_market_cap with small values."""
        assert format_market_cap(500) == "500.0"
        assert format_market_cap(999) == "999.0"

    def test_format_market_cap_thousands(self):
        """Test format_market_cap with thousands."""
        assert format_market_cap(1500) == "1.5K"
        assert format_market_cap(999999) == "1000.0K"

    def test_format_market_cap_millions(self):
        """Test format_market_cap with millions."""
        assert format_market_cap(1_500_000) == "1.5M"
        assert format_market_cap(999_999_999) == "1000.0M"

    def test_format_market_cap_billions(self):
        """Test format_market_cap with billions."""
        assert format_market_cap(1_500_000_000) == "1.5B"
        assert format_market_cap(2_500_000_000_000) == "2.5T"


class TestGetFinancials:
    """Tests for get_financials function."""

    def test_get_financials_success(self):
        """Test get_financials with complete info."""
        mock_ticker = MagicMock()
        mock_ticker.info = {
            "marketCap": 2_500_000_000_000,
            "trailingPE": 28.5,
            "dividendYield": 0.005,
            "fiftyTwoWeekHigh": 180.0,
            "fiftyTwoWeekLow": 120.0,
        }

        with patch("function.stock.yf.Ticker", return_value=mock_ticker):
            result = get_financials("AAPL")

        assert result["market_cap"] == 2_500_000_000_000
        assert result["pe_ratio"] == 28.5
        assert result["dividend_yield"] == 0.005
        assert result["high_52wk"] == 180.0
        assert result["low_52wk"] == 120.0

    def test_get_financials_missing_fields(self):
        """Test get_financials with missing info fields."""
        mock_ticker = MagicMock()
        mock_ticker.info = {}

        with patch("function.stock.yf.Ticker", return_value=mock_ticker):
            result = get_financials("UNKNOWN")

        assert result["market_cap"] is None
        assert result["pe_ratio"] is None
        assert result["dividend_yield"] is None


class TestPrintStock:
    """Tests for print_stock function."""

    @patch("function.stock.calculate_returns")
    @patch("function.stock.get_financials")
    def test_print_stock_success(self, mock_financials, mock_returns, mock_printer):
        """Test print_stock with successful data."""
        mock_returns.return_value = {"week": 2.5, "month": 5.0, "year": 15.0}
        mock_financials.return_value = {
            "market_cap": 2_500_000_000_000,
            "pe_ratio": 28.5,
            "dividend_yield": 0.005,
            "high_52wk": 180.0,
            "low_52wk": 120.0,
        }

        print_stock(mock_printer, "AAPL")

        text_calls = [call[0][0] for call in mock_printer.text.call_args_list]
        output = "".join(text_calls)
        assert "AAPL:" in output
        assert "+2.5%" in output or "2.5%" in output
        assert "2.5T" in output
        assert "28.5" in output

    @patch("function.stock.calculate_returns")
    def test_print_stock_handles_error(self, mock_returns, mock_printer):
        """Test print_stock handles calculation errors."""
        mock_returns.side_effect = Exception("API Error")

        print_stock(mock_printer, "INVALID")

        text_calls = [call[0][0] for call in mock_printer.text.call_args_list]
        output = "".join(text_calls)
        assert "Could not fetch data" in output