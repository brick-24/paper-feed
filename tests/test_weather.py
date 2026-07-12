"""Tests for weather module."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from function.weather import get_weather, print_weather


class TestGetWeather:
    """Tests for get_weather function."""

    @patch("function.weather.requests.get")
    def test_get_weather_success(self, mock_get):
        """Test get_weather with successful API response."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "current_condition": [
                {
                    "weatherDesc": [{"value": "Sunny"}],
                    "temp_C": "25",
                    "FeelsLikeC": "27",
                    "humidity": "60",
                    "precipMM": "0.0",
                }
            ],
            "weather": [
                {
                    "astronomy": [
                        {
                            "sunrise": "06:00",
                            "sunset": "18:30",
                            "moonrise": "19:00",
                            "moonset": "07:00",
                            "moon_phase": "Waxing Crescent",
                            "moon_illumination": "25",
                        }
                    ],
                    "hourly": [
                        {"time": "0", "chanceofrain": "0"},
                        {"time": "300", "chanceofrain": "10"},
                        {"time": "600", "chanceofrain": "20"},
                        {"time": "900", "chanceofrain": "30"},
                    ],
                }
            ],
        }
        mock_get.return_value = mock_response

        result = get_weather("Delhi")

        assert result["description"] == "Sunny"
        assert result["temp"] == "25"
        assert result["feels_like"] == "27"
        assert result["humidity"] == "60"
        assert result["sunrise"] == "06:00"
        assert result["sunset"] == "18:30"

    @patch("function.weather.requests.get")
    def test_get_weather_raises_on_error(self, mock_get):
        """Test get_weather raises on HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        with pytest.raises(Exception):
            get_weather("InvalidCity")


class TestPrintWeather:
    """Tests for print_weather function."""

    @patch("function.weather.get_weather")
    def test_print_weather_success(self, mock_get_weather, mock_printer):
        """Test print_weather with valid data."""
        mock_get_weather.return_value = {
            "description": "Partly Cloudy",
            "temp": "22",
            "feels_like": "24",
            "humidity": "55",
            "chance_of_rain": "10",
            "precip": "0.0",
            "sunrise": "06:15",
            "sunset": "18:45",
            "moonrise": "20:00",
            "moonset": "08:00",
            "moon_phase": "Full Moon",
            "moon_illumination": "95",
        }

        print_weather(mock_printer, "Mumbai")

        # Verify printer was called
        text_calls = [call[0][0] for call in mock_printer.text.call_args_list]
        output = "".join(text_calls)
        assert "WEATHER:" in output
        assert "Partly Cloudy" in output
        assert "22 °C" in output
        assert "55%" in output

    @patch("function.weather.get_weather")
    def test_print_weather_propagates_api_error(self, mock_get_weather, mock_printer):
        """Test print_weather propagates API errors."""
        mock_get_weather.side_effect = Exception("Network error")

        # Should raise the exception
        with pytest.raises(Exception, match="Network error"):
            print_weather(mock_printer, "Tokyo")