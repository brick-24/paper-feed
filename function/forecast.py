"""7-day weather forecast using Open-Meteo API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from function.http_client import get_json
from printer import hr, print_title


WEATHER_CODES = {
    0: "Clear",
    1: "Mostly Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    56: "Freezing Drizzle",
    57: "Freezing Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    66: "Freezing Rain",
    67: "Freezing Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Rain Showers",
    81: "Rain Showers",
    82: "Heavy Showers",
    85: "Snow Showers",
    86: "Heavy Snow",
    95: "Thunderstorm",
    96: "Thunderstorm",
    99: "Severe Storm",
}


def get_weekly_weather(city: str) -> list[dict[str, Any]]:
    """Fetch 7-day forecast for a city.

    Args:
        city: City name to geocode and fetch forecast for.

    Returns:
        List of daily forecast dicts with keys: date, description, high, low, rain.

    Raises:
        ValueError: If city not found.
        requests.HTTPError: On API errors.
    """
    # Geocode city -> latitude/longitude
    geo = get_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        timeout=(5, 10),
    )

    results = geo.get("results")
    if not results:
        raise ValueError(f"City '{city}' not found.")

    lat = results[0]["latitude"]
    lon = results[0]["longitude"]

    # Fetch forecast
    resp = get_json(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": (
                "weathercode,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max"
            ),
            "forecast_days": 7,
            "timezone": "auto",
        },
        timeout=(5, 15),
    )

    data = resp["daily"]

    forecast = []
    for i in range(len(data["time"])):
        forecast.append({
            "date": datetime.strptime(data["time"][i], "%Y-%m-%d").strftime("%a %d"),
            "description": WEATHER_CODES.get(data["weathercode"][i], "Unknown"),
            "high": round(data["temperature_2m_max"][i]),
            "low": round(data["temperature_2m_min"][i]),
            "rain": data["precipitation_probability_max"][i] or 0,
        })

    return forecast


def print_weekly_weather(printer, city: str) -> None:
    """Print 7-day forecast table."""
    forecast = get_weekly_weather(city)

    print_title(printer, "FORECAST:")
    hr(printer)

    printer.set(align="left", bold=False, width=1, height=1)

    printer.text(f"{'DAY':^10}{'HI/LO':^10}{'RAIN':^10}\n")

    for day in forecast:
        printer.text(
            f"{day['date']:^10}"
            f"{f'{day['high']}/{day['low']}°C':^10}"
            f"{f'{day['rain']}%':^10}\n"
        )

    printer.ln()