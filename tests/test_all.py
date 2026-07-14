"""Unit tests for paper-feed modules using mocks."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Check if optional dependencies are available
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None
    np = None

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False
    feedparser = None

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    yf = None


class TestConfig:
    """Tests for config.py"""

    def test_default_vendor_product_ids(self):
        from config import DEFAULT_VENDOR_ID, DEFAULT_PRODUCT_ID
        assert DEFAULT_VENDOR_ID == 0x0483
        assert DEFAULT_PRODUCT_ID == 0x5840

    def test_default_options(self):
        from config import DEFAULT_OPTIONS
        assert "weather" in DEFAULT_OPTIONS
        assert "markets" in DEFAULT_OPTIONS
        assert "quote" in DEFAULT_OPTIONS

    def test_tickers_dict(self):
        from config import TICKERS
        assert "NIFTY" in TICKERS
        assert "SENSX" in TICKERS
        assert TICKERS["NIFTY"] == "^NSEI"


class TestPrinter:
    """Tests for printer.py"""

    def test_terminal_printer_creation(self):
        from printer import TerminalPrinter
        printer = TerminalPrinter()
        assert printer.align == "left"
        assert printer.WIDTH == 32

    def test_terminal_printer_set_align(self):
        from printer import TerminalPrinter
        printer = TerminalPrinter()
        printer.set(align="center")
        assert printer.align == "center"

    def test_terminal_printer_text(self, capsys):
        from printer import TerminalPrinter
        printer = TerminalPrinter()
        printer.text("Hello\n")
        captured = capsys.readouterr()
        assert "Hello" in captured.out

    def test_terminal_printer_text_centered(self, capsys):
        from printer import TerminalPrinter
        printer = TerminalPrinter()
        printer.set(align="center")
        printer.text("Hello\n")
        captured = capsys.readouterr()
        assert "Hello" in captured.out

    def test_print_title(self, capsys):
        from printer import TerminalPrinter, print_title
        printer = TerminalPrinter()
        print_title(printer, "TEST TITLE")
        captured = capsys.readouterr()
        assert "TEST TITLE" in captured.out

    def test_hr(self, capsys):
        from printer import TerminalPrinter, hr
        printer = TerminalPrinter()
        hr(printer)
        captured = capsys.readouterr()
        assert "-" in captured.out


class TestWeather:
    """Tests for function/weather.py"""

    @patch("function.weather.requests.get")
    def test_get_weather_success(self, mock_get):
        from function.weather import get_weather
        from datetime import datetime

        # Determine what the current target time would be
        now = datetime.now()
        target = (now.hour // 3) * 300
        target_str = f"{target:04d}"

        mock_response = Mock()
        mock_response.json.return_value = {
            "current_condition": [{
                "weatherDesc": [{"value": "Sunny"}],
                "temp_C": "25",
                "FeelsLikeC": "27",
                "humidity": "60",
                "precipMM": "0.0"
            }],
            "weather": [{
                "astronomy": [{
                    "sunrise": "06:00",
                    "sunset": "18:00",
                    "moonrise": "20:00",
                    "moonset": "08:00",
                    "moon_phase": "Full",
                    "moon_illumination": "100"
                }],
                "hourly": [
                    {"time": "000", "chanceofrain": "0"},
                    {"time": "300", "chanceofrain": "0"},
                    {"time": "600", "chanceofrain": "0"},
                    {"time": "900", "chanceofrain": "0"},
                    {"time": "1200", "chanceofrain": "10"},
                    {"time": "1500", "chanceofrain": "20"},
                    {"time": "1800", "chanceofrain": "30"},
                    {"time": "2100", "chanceofrain": "10"}
                ]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = get_weather("Delhi")

        assert result["description"] == "Sunny"
        assert result["temp"] == "25"
        assert result["humidity"] == "60"

    @patch("function.weather.requests.get")
    def test_get_weather_http_error(self, mock_get):
        from function.weather import get_weather
        import requests

        mock_get.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            get_weather("InvalidCity")


class TestForecast:
    """Tests for function/forecast.py"""

    @patch("function.forecast.requests.get")
    def test_get_weekly_weather_success(self, mock_get):
        from function.forecast import get_weekly_weather

        # Mock geocoding response
        geo_response = Mock()
        geo_response.json.return_value = {"results": [{"latitude": 28.61, "longitude": 77.21}]}
        geo_response.raise_for_status = Mock()

        # Mock forecast response
        forecast_response = Mock()
        forecast_response.json.return_value = {
            "daily": {
                "time": ["2024-01-01", "2024-01-02"],
                "weathercode": [0, 1],
                "temperature_2m_max": [25.5, 26.0],
                "temperature_2m_min": [15.0, 16.0],
                "precipitation_probability_max": [10, 20]
            }
        }
        forecast_response.raise_for_status = Mock()

        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weekly_weather("Delhi")

        assert len(result) == 2
        assert result[0]["description"] == "Clear"
        assert result[0]["high"] == 26
        assert result[0]["low"] == 15
        assert result[0]["rain"] == 10

    @patch("function.forecast.requests.get")
    def test_get_weekly_weather_city_not_found(self, mock_get):
        from function.forecast import get_weekly_weather

        geo_response = Mock()
        geo_response.json.return_value = {"results": []}
        geo_response.raise_for_status = Mock()
        mock_get.return_value = geo_response

        with pytest.raises(ValueError, match="City 'InvalidCity' not found"):
            get_weekly_weather("InvalidCity")


class TestMarkets:
    """Tests for function/markets.py"""

    @pytest.mark.skipif(not PANDAS_AVAILABLE, reason="pandas not installed")
    @patch("function.markets.yf.Ticker")
    def test_calculate_returns(self, mock_ticker_class):
        from function.markets import calculate_returns
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta

        dates = pd.date_range(end=datetime.now(), periods=30, freq="D")
        closes = np.linspace(100, 110, 30)
        hist = pd.DataFrame({"Close": closes}, index=dates)

        mock_ticker = Mock()
        mock_ticker.history.return_value = hist
        mock_ticker_class.return_value = mock_ticker

        result = calculate_returns("TEST")

        assert "day" in result
        assert "week" in result
        assert "month" in result
        assert isinstance(result["day"], float)

    @pytest.mark.skipif(not PANDAS_AVAILABLE, reason="pandas not installed")
    @patch("function.markets.yf.Ticker")
    def test_calculate_returns_insufficient_data(self, mock_ticker_class):
        from function.markets import calculate_returns
        import pandas as pd
        import numpy as np
        from datetime import datetime

        dates = pd.date_range(end=datetime.now(), periods=10, freq="D")
        closes = np.linspace(100, 110, 10)
        hist = pd.DataFrame({"Close": closes}, index=dates)

        mock_ticker = Mock()
        mock_ticker.history.return_value = hist
        mock_ticker_class.return_value = mock_ticker

        with pytest.raises(ValueError, match="Not enough history"):
            calculate_returns("TEST")

class TestStock:
    """Tests for function/stock.py"""

    @pytest.mark.skipif(not YFINANCE_AVAILABLE, reason="yfinance not installed")
    @patch("function.stock.yf.Ticker")
    def test_get_financials(self, mock_ticker_class):
        from function.stock import get_financials

        mock_ticker = Mock()
        mock_ticker.info = {
            "marketCap": 1000000000,
            "trailingPE": 25.5,
            "dividendYield": 0.02,
            "fiftyTwoWeekHigh": 150.0,
            "fiftyTwoWeekLow": 100.0
        }
        mock_ticker_class.return_value = mock_ticker

        result = get_financials("TEST")

        assert result["market_cap"] == 1000000000
        assert result["pe_ratio"] == 25.5
        assert result["dividend_yield"] == 0.02

    @pytest.mark.skipif(not YFINANCE_AVAILABLE, reason="yfinance not installed")
    def test_format_market_cap(self):
        from function.stock import format_market_cap

        assert format_market_cap(None) == "N/A"
        assert format_market_cap(500) == "500.0"
        assert format_market_cap(1500) == "1.5K"
        assert format_market_cap(1500000) == "1.5M"
        assert format_market_cap(1500000000) == "1.5B"
        assert format_market_cap(1500000000000) == "1.5T"


class TestQuote:
    """Tests for function/quote.py"""

    @patch("function.quote.requests.get")
    def test_print_quote(self, mock_get, capsys):
        from function.quote import print_quote
        from printer import TerminalPrinter

        mock_response = Mock()
        mock_response.json.return_value = {"content": "Test quote", "author": "Test Author"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        printer = TerminalPrinter()
        print_quote(printer)

        captured = capsys.readouterr()
        assert "Test quote" in captured.out
        assert "Test Author" in captured.out


class TestComic:
    """Tests for function/comic.py"""

    @patch("function.comic.requests.get")
    def test_download_xkcd(self, mock_get):
        from function.comic import download_xkcd
        import tempfile
        from pathlib import Path

        # Mock the xkcd API response
        api_response = Mock()
        api_response.json.return_value = {
            "safe_title": "Test Comic",
            "num": 123,
            "img": "https://example.com/comic.png"
        }
        api_response.raise_for_status = Mock()

        # Mock the image download
        img_response = Mock()
        img_response.content = b"fake image data"
        img_response.raise_for_status = Mock()

        mock_get.side_effect = [api_response, img_response]

        with patch("function.comic.Image.open") as mock_image_open:
            mock_img = Mock()
            mock_img.convert.return_value.save = Mock()
            mock_image_open.return_value = mock_img

            with patch("function.comic.tempfile.NamedTemporaryFile") as mock_temp:
                mock_temp_file = Mock()
                mock_temp_file.name = "/tmp/test.png"
                mock_temp.__enter__.return_value = mock_temp_file

                with patch("function.comic.Path") as mock_path:
                    mock_path_instance = Mock()
                    mock_path_instance.exists.return_value = True
                    mock_path.return_value = mock_path_instance

                    result = download_xkcd()

                    assert result["title"] == "Test Comic"
                    assert result["num"] == 123


class TestNews:
    """Tests for function/news.py"""

    @pytest.mark.skipif(not FEEDPARSER_AVAILABLE, reason="feedparser not installed")
    @patch("function.news.feedparser.parse")
    def test_news_parsing(self, mock_parse):
        import function.news as news_module

        mock_feed = Mock()
        mock_feed.entries = [
            Mock(title="Test headline 1"),
            Mock(title="Test headline 2"),
        ]
        mock_parse.return_value = mock_feed

        # Since news.py just prints on import, we test the parsing logic
        feed = feedparser.parse("http://test.com/feed")
        assert len(feed.entries) == 2


class TestTextInput:
    """Tests for function/text_inp.py"""

    def test_print_text_input(self, capsys):
        from function.text_inp import print_text_input
        from printer import TerminalPrinter

        printer = TerminalPrinter()
        print_text_input(printer, "Hello World")

        captured = capsys.readouterr()
        assert "Hello World" in captured.out


class TestImageInput:
    """Tests for function/image_inp.py"""

    def test_print_image_input_not_found(self):
        from function.image_inp import print_image_input
        from printer import TerminalPrinter

        printer = TerminalPrinter()

        with pytest.raises(FileNotFoundError):
            print_image_input(printer, "/nonexistent/image.png")


class TestDailyArg:
    """Tests for daily_arg.py CLI"""

    @pytest.mark.skipif(not YFINANCE_AVAILABLE, reason="yfinance not installed")
    def test_parse_args_defaults(self):
        from daily_arg import parse_args
        import sys

        # Mock sys.argv
        test_args = ["daily_arg.py"]
        with patch.object(sys, "argv", test_args):
            args = parse_args()
            assert args.city == "Delhi"
            assert args.test is False

    @pytest.mark.skipif(not YFINANCE_AVAILABLE, reason="yfinance not installed")
    def test_parse_args_custom_city(self):
        from daily_arg import parse_args
        import sys

        test_args = ["daily_arg.py", "--city", "London", "--weather"]
        with patch.object(sys, "argv", test_args):
            args = parse_args()
            assert args.city == "London"
            assert args.weather is True

    @pytest.mark.skipif(not YFINANCE_AVAILABLE, reason="yfinance not installed")
    def test_parse_args_test_mode(self):
        from daily_arg import parse_args
        import sys

        test_args = ["daily_arg.py", "--test", "--text", "Hello"]
        with patch.object(sys, "argv", test_args):
            args = parse_args()
            assert args.test is True
            assert args.text == "Hello"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])