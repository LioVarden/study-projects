import os
import requests
from dotenv import load_dotenv


load_dotenv()

# API key for OpenWeather service
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    """
    Fetch current weather for a given city using OpenWeather API.
    Returns formatted weather string or None if city is not found.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "en"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # API returns cod != 200 if city is not found
    if data.get("cod") != 200:
        return None

    city_name = data["name"]
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]

    return f"{city_name}\nTemperature: {temp}°C\nWeather: {description}"