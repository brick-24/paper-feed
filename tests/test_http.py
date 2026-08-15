import requests
from function.forecast import get_weekly_weather
from function.news import fetch_news
from function.weather import get_weather

def test_weather_http_check():
    weather = get_weather("Jaipur")

    assert weather["description"]
    assert weather["temp"] != ""
    assert weather["humidity"] != ""
    assert weather["sunrise"]
    assert weather["sunset"]


def test_forecast_http_check():
    forecast = get_weekly_weather("Jaipur")

    assert len(forecast) == 7
    assert forecast[0]["date"]
    assert forecast[0]["description"]
    assert isinstance(forecast[0]["high"], int)
    assert isinstance(forecast[0]["low"], int)
    assert forecast[0]["rain"] is not None


def test_news_rss_http_check():
    headlines = fetch_news(limit=1)

    assert len(headlines) == 1
    assert headlines[0].strip()
