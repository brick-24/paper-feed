import requests

from printer import hr, print_title


def get_weather(city):
    r = requests.get(
        f"https://wttr.in/{city}",
        params={"format": "j1"},
        timeout=10,
    )
    r.raise_for_status()

    current = r.json()["current_condition"][0]

    return {
        "description": current["weatherDesc"][0]["value"],
        "temp": current["temp_C"],
        "feels_like": current["FeelsLikeC"],
        "humidity": current["humidity"],
        "precip": current["precipMM"],
    }


def print_weather(printer, city):
    weather = get_weather(city)

    hr(printer)

    print_title(printer, "WEATHER:")

    hr(printer)

    printer.text(f"{weather['description']}\n\n")
    printer.text(f"Temp:            {weather['temp']} C\n")
    printer.text(f"Feels Like:      {weather['feels_like']} C\n")
    printer.text(f"Humidity:        {weather['humidity']}%\n")
    printer.text(f"Rain:            {weather['precip']} mm\n")

    hr(printer)
