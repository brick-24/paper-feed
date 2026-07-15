import requests
from datetime import datetime
from printer import hr, print_title
from function.http_client import get_json


def get_weather(city):
    data = get_json(
        f"https://wttr.in/{city}",
        params={"format": "j1"},
        timeout=(5, 10),
    )

    current = data["current_condition"][0]
    today = data["weather"][0]
    astronomy = today["astronomy"][0]
    hourly = today["hourly"]

    now = datetime.now()
    target = (now.hour // 3) * 300

    forecast = min(
        hourly,
        key=lambda h: abs(int(h["time"]) - target)
    )

    return {
        "description": current["weatherDesc"][0]["value"],
        "temp": current["temp_C"],
        "feels_like": current["FeelsLikeC"],
        "humidity": current["humidity"],
        "chance_of_rain": forecast["chanceofrain"],
        "precip": current["precipMM"],
        "sunrise": astronomy["sunrise"],
        "sunset": astronomy["sunset"],
        "moonrise": astronomy["moonrise"],
        "moonset": astronomy["moonset"],
        "moon_phase": astronomy["moon_phase"],
        "moon_illumination": astronomy["moon_illumination"],
    }


def print_weather(printer, city):
    weather = get_weather(city)
    print_title(printer, "WEATHER:")

    hr(printer)
    printer.set(align="center", bold = False, width = 1, height = 1)
    printer.text(f"{weather['description']}\n\n")

    printer.set(align="left", bold = False, width = 1, height = 1)
    printer.text(f"Temperature:     {weather['temp']} °C\n")
    printer.text(f"Feels Like:      {weather['feels_like']} °C\n")
    printer.text(f"Humidity:        {weather['humidity']}%\n")
    printer.text(f"Chance of Rain:  {weather['chance_of_rain']}%\n")
    # printer.text(f"Rain:            {weather['precip']} mm\n")
    printer.text(f"Sunrise:         {weather['sunrise']}\n")
    printer.text(f"Sunset:          {weather['sunset']}\n")
    printer.text(f"Moon:            {weather['moon_phase']}\n") # ({weather['moon_illumination']}%)

    # hr(printer)
    printer.ln()