import requests
from datetime import datetime

# using open meteo as wttr.in does not support weekly forecast

def get_weekly_weather(city):
    # Geocode city -> latitude/longitude
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1,
        },
        timeout=10,
    )
    geo.raise_for_status()

    results = geo.json().get("results")
    if not results:
        raise ValueError(f"City '{city}' not found.")

    lat = results[0]["latitude"]
    lon = results[0]["longitude"]

    r = requests.get(
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
        timeout=10,
    )
    r.raise_for_status()

    data = r.json()["daily"]

    weather_codes = {
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

    forecast = []

    for i in range(len(data["time"])):
        forecast.append({
            "date": datetime.strptime(
                data["time"][i], "%Y-%m-%d"
            ).strftime("%a %d"),
            "description": weather_codes.get(
                data["weathercode"][i], "Unknown"
            ),
            "high": round(data["temperature_2m_max"][i]),
            "low": round(data["temperature_2m_min"][i]),
            "rain": data["precipitation_probability_max"][i] or 0,
        })

    return forecast

from printer import hr, print_title

def print_weekly_weather(printer, city):
    forecast = get_weekly_weather(city)

    print_title(printer, "FORECAST:")
    hr(printer)

    printer.set(
        align="left",
        bold=False,
        width=1,
        height=1,
    )
    
    # char allignment 
    # {value:<N} = left-align in a field N chars wide
    # {value:>N} = right-align in a field N chars wide
    # {value:^N} = center-align in a field N chars wide

    printer.text(f"{'DAY':^10}{'HI/LO':^10}{'RAIN':^10}\n")

    for day in forecast:
        printer.text(
            f"{day['date']:^10}"
            f"{f'{day['high']}/{day['low']}°C':^10}"
            f"{f'{day['rain']}%':^10}\n"
        )

        # printer.text(f"         {day['description']}\n")
    printer.ln()