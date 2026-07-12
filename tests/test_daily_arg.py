"""Tests for daily_arg module."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import daily_arg


class TestParseArgs:
    """Tests for parse_args function."""

    def test_parse_args_defaults(self):
        """Test parse_args with no arguments."""
        with patch("sys.argv", ["daily_arg.py"]):
            args = daily_arg.parse_args()

        assert args.xkcd is False
        assert args.weather is False
        assert args.markets is False
        assert args.quote is False
        assert args.city == "Delhi"
        assert args.text is None
        assert args.image is None
        assert args.test is False
        assert args.stock is None
        assert args.forecast is False

    def test_parse_args_all_flags(self):
        """Test parse_args with all flags."""
        test_args = [
            "daily_arg.py",
            "--xkcd",
            "--weather",
            "--markets",
            "--quote",
            "--city",
            "Mumbai",
            "--text",
            "Hello",
            "--image",
            "/path/img.png",
            "--test",
            "--stock",
            "AAPL",
            "--forecast",
        ]
        with patch("sys.argv", test_args):
            args = daily_arg.parse_args()

        assert args.xkcd is True
        assert args.weather is True
        assert args.markets is True
        assert args.quote is True
        assert args.city == "Mumbai"
        assert args.text == "Hello"
        assert args.image == "/path/img.png"
        assert args.test is True
        assert args.stock == "AAPL"
        assert args.forecast is True


class TestMain:
    """Tests for main function."""

    @patch("daily_arg.create_printer")
    @patch("daily_arg.print_weather")
    @patch("daily_arg.print_markets")
    @patch("daily_arg.print_quote")
    def test_main_default_options(self, mock_quote, mock_markets, mock_weather, mock_create_printer):
        """Test main with default options (no args)."""
        mock_printer = MagicMock()
        mock_create_printer.return_value = mock_printer

        with patch("sys.argv", ["daily_arg.py"]):
            daily_arg.main()

        mock_weather.assert_called_once()
        mock_markets.assert_called_once()
        mock_quote.assert_called_once()

    @patch("daily_arg.TerminalPrinter")
    @patch("daily_arg.print_weather")
    @patch("daily_arg.print_xkcd")
    def test_main_test_mode(self, mock_xkcd, mock_weather, mock_terminal_printer):
        """Test main in test mode uses TerminalPrinter."""
        mock_printer = MagicMock()
        mock_terminal_printer.return_value = mock_printer

        with patch("sys.argv", ["daily_arg.py", "--test", "--weather", "--xkcd"]):
            daily_arg.main()

        mock_terminal_printer.assert_called_once()
        mock_weather.assert_called_once()
        mock_xkcd.assert_called_once()

    @patch("daily_arg.TerminalPrinter")
    @patch("daily_arg.print_text_input")
    def test_main_custom_text(self, mock_text, mock_terminal_printer):
        """Test main with custom text."""
        mock_printer = MagicMock()
        mock_terminal_printer.return_value = mock_printer

        with patch("sys.argv", ["daily_arg.py", "--test", "--text", "Hello World"]):
            daily_arg.main()

        mock_text.assert_called_once_with(mock_printer, "Hello World")

    @patch("daily_arg.TerminalPrinter")
    @patch("daily_arg.print_image_input")
    def test_main_custom_image(self, mock_image, mock_terminal_printer):
        """Test main with custom image."""
        mock_printer = MagicMock()
        mock_terminal_printer.return_value = mock_printer

        with patch("sys.argv", ["daily_arg.py", "--test", "--image", "/tmp/img.png"]):
            daily_arg.main()

        mock_image.assert_called_once_with(mock_printer, "/tmp/img.png")

    @patch("daily_arg.TerminalPrinter")
    @patch("daily_arg.print_stock")
    def test_main_stock(self, mock_stock, mock_terminal_printer):
        """Test main with stock option."""
        mock_printer = MagicMock()
        mock_terminal_printer.return_value = mock_printer

        with patch("sys.argv", ["daily_arg.py", "--test", "--stock", "AAPL"]):
            daily_arg.main()

        mock_stock.assert_called_once_with(mock_printer, "AAPL")

    @patch("daily_arg.TerminalPrinter")
    @patch("daily_arg.print_weekly_weather")
    def test_main_forecast(self, mock_forecast, mock_terminal_printer):
        """Test main with forecast option."""
        mock_printer = MagicMock()
        mock_terminal_printer.return_value = mock_printer

        with patch("sys.argv", ["daily_arg.py", "--test", "--forecast", "--city", "London"]):
            daily_arg.main()

        mock_forecast.assert_called_once_with(mock_printer, "London")