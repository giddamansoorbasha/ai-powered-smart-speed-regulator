import httpx
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def fetch_live_weather(city: str) -> dict:
    """
    Fetches real-time weather from OpenWeatherMap API by city name.
    Maps weather condition to: clear, rainy, foggy
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            })
            response.raise_for_status()
            data = response.json()

        weather_main = data["weather"][0]["main"].lower()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        city_name = data["name"]

        # Map OpenWeatherMap conditions → our 3 categories
        if any(w in weather_main for w in ["rain", "drizzle", "thunderstorm", "snow"]):
            condition = "rainy"
        elif any(w in weather_main for w in ["fog", "mist", "haze", "smoke", "dust"]):
            condition = "foggy"
        else:
            condition = "clear"

        return {
            "condition": condition,
            "raw": weather_main,
            "description": description,
            "temperature_c": temp,
            "city": city_name,
            "source": "live"
        }

    except httpx.HTTPStatusError as e:
        # City not found or bad request → fallback
        return {
            "condition": "clear",
            "raw": "unknown",
            "description": f"Could not fetch weather for '{city}' — using clear as default",
            "temperature_c": None,
            "city": city,
            "source": "fallback"
        }
    except Exception:
        return {
            "condition": "clear",
            "raw": "error",
            "description": "Weather API error — using clear as default",
            "temperature_c": None,
            "city": city,
            "source": "fallback"
        }