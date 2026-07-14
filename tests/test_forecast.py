"""Tests for function.forecast module."""

from unittest.mock import MagicMock, patch

import pytest

from function.forecast import get_weekly_weather, print_weekly_weather


class TestGetWeeklyWeather:
    """Tests for get_weekly_weather function."""

    @patch("function.forecast.requests.get")
    def test_get_weekly_weather_success(self, mock_get, sample_forecast_data):
        # Mock geocoding response
        geo_response = MagicMock()
        geo_response.raise_for_status = MagicMock()
        geo_response.json.return_value = {"results": [{"latitude": 28.6, "longitude": 77.2}]}

        # Mock forecast response
        forecast_response = MagicMock()
        forecast_response.raise_for_status = MagicMock()
        forecast_response.json.return_value = sample_forecast_data

        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weekly_weather("Delhi")

        assert isinstance(result, list)
        assert len(result) == 3
        # Date format: Mon 14 (from 2026-07-14 which is a Tuesday)
        assert result[0]["high"] == 32  # round(32.5) = 32
        assert result[0]["low"] == 24
        assert result[0]["rain"] == 0
        assert result[1]["description"] == "Mostly Clear"
        assert result[2]["description"] == "Light Rain"
        assert result[2]["rain"] == 80

    @patch("function.forecast.requests.get")
    def test_get_weekly_weather_city_not_found(self, mock_get):
        geo_response = MagicMock()
        geo_response.raise_for_status = MagicMock()
        geo_response.json.return_value = {"results": []}
        mock_get.return_value = geo_response

        with pytest.raises(ValueError, match="City 'UnknownCity' not found"):
            get_weekly_weather("UnknownCity")

    @patch("function.forecast.requests.get")
    def test_get_weekly_weather_geocode_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            get_weekly_weather("Delhi")

    @patch("function.forecast.requests.get")
    def test_get_weekly_weather_forecast_api_failure(self, mock_get):
        geo_response = MagicMock()
        geo_response.raise_for_status = MagicMock()
        geo_response.json.return_value = {"results": [{"latitude": 28.6, "longitude": 77.2}]}

        forecast_response = MagicMock()
        forecast_response.raise_for_status.side_effect = Exception("API error")

        mock_get.side_effect = [geo_response, forecast_response]

        with pytest.raises(Exception, match="API error"):
            get_weekly_weather("Delhi")

    @patch("function.forecast.requests.get")
    def test_get_weekly_weather_unknown_weather_code(self, mock_get):
        """Test handling of unknown weather codes."""
        geo_response = MagicMock()
        geo_response.raise_for_status = MagicMock()
        geo_response.json.return_value = {"results": [{"latitude": 28.6, "longitude": 77.2}]}

        forecast_response = MagicMock()
        forecast_response.raise_for_status = MagicMock()
        forecast_response.json.return_value = {
            "daily": {
                "time": ["2026-07-14"],
                "weathercode": [999],  # Unknown code
                "temperature_2m_max": [30.0],
                "temperature_2m_min": [20.0],
                "precipitation_probability_max": [0],
            }
        }

        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weekly_weather("Delhi")

        assert result[0]["description"] == "Unknown"


class TestPrintWeeklyWeather:
    """Tests for print_weekly_weather function."""

    @patch("function.forecast.get_weekly_weather")
    def test_print_weekly_weather_formats_output(self, mock_get_weather, mock_printer):
        mock_get_weather.return_value = [
            {"date": "Mon 14", "high": 33, "low": 24, "rain": 0, "description": "Clear"},
            {"date": "Tue 15", "high": 31, "low": 23, "rain": 50, "description": "Rain"},
        ]

        print_weekly_weather(mock_printer, "Delhi")

        mock_get_weather.assert_called_once_with("Delhi")
        mock_printer.set.assert_called()
        mock_printer.text.assert_called()
        mock_printer.ln.assert_called()

    @patch("function.forecast.get_weekly_weather")
    def test_print_weekly_weather_table_format(self, mock_get_weather, mock_printer):
        mock_get_weather.return_value = [
            {"date": "Mon 14", "high": 33, "low": 24, "rain": 0, "description": "Clear"},
        ]

        print_weekly_weather(mock_printer, "Delhi")

        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "DAY" in output
        assert "HI/LO" in output
        assert "RAIN" in output
        assert "33/24°C" in output
        assert "0%" in output