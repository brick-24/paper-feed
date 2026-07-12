"""Tests for markets module."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock yfinance before importing markets
with patch.dict("sys.modules", {"yfinance": MagicMock()}):
    from function.markets import calculate_returns, print_markets


class TestCalculateReturns:
    """Tests for calculate_returns function."""

    def test_calculate_returns_insufficient_history(self):
        """Test calculate_returns raises with insufficient history."""
        mock_ticker = MagicMock()
        mock_hist = MagicMock()
        mock_closes = MagicMock()
        mock_dropped = MagicMock()
        mock_dropped.__len__ = MagicMock(return_value=10)
        mock_closes.dropna.return_value = mock_dropped
        mock_hist.__getitem__.return_value = mock_closes
        mock_ticker.history.return_value = mock_hist

        with patch("function.markets.yf.Ticker", return_value=mock_ticker):
            with pytest.raises(ValueError, match="Not enough history"):
                calculate_returns("AAPL")


class TestPrintMarkets:
    """Tests for print_markets function."""

    @patch("function.markets.calculate_returns")
    def test_print_markets_success(self, mock_calc, mock_printer):
        """Test print_markets with successful data."""
        mock_calc.side_effect = [
            {"day": 1.5, "week": 2.0, "month": 5.0},
            {"day": -0.5, "week": 1.0, "month": -2.0},
        ]

        with patch("function.markets.TICKERS", {"NIFTY": "^NSEI", "SENSX": "^BSESN"}):
            print_markets(mock_printer)

        mock_printer.text.assert_called()
        text_calls = [call[0][0] for call in mock_printer.text.call_args_list]
        output = "".join(text_calls)
        assert "MARKETS:" in output
        assert "NIFTY" in output
        assert "SENSX" in output

    @patch("function.markets.calculate_returns")
    def test_print_markets_handles_errors(self, mock_calc, mock_printer):
        """Test print_markets handles calculation errors."""
        mock_calc.side_effect = [
            {"day": 1.0, "week": 2.0, "month": 3.0},
            Exception("API Error"),
        ]

        with patch("function.markets.TICKERS", {"GOOD": "GOOD", "BAD": "BAD"}):
            print_markets(mock_printer)

        text_calls = [call[0][0] for call in mock_printer.text.call_args_list]
        output = "".join(text_calls)
        assert "ERR" in output or "GOOD" in output