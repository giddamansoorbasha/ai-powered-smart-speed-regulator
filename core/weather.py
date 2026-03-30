VALID_WEATHER_CONDITIONS = ["clear", "rainy", "foggy"]

def validate_weather(weather: str) -> str:
    """
    Validates and returns weather condition.
    Defaults to 'clear' if invalid input given.
    """
    weather = weather.lower().strip()
    
    if weather in VALID_WEATHER_CONDITIONS:
        return weather
    
    return "clear"  # Default fallback


def get_weather_description(weather: str) -> str:
    """
    Returns human readable description for presentation/UI.
    """
    descriptions = {
        "clear":  "Clear conditions — normal speed limits apply.",
        "rainy":  "Rainy conditions — speed reduced by 15 kmph for safety.",
        "foggy":  "Foggy conditions — speed reduced by 20 kmph for safety.",
    }
    
    return descriptions.get(weather, "Unknown condition — applying safe defaults.")


"""
Weather module validates input and provides human-readable safety descriptions. 
In a real deployment, this connects to OpenWeatherMap API to fetch live weather data automatically. 
For our demo, user selects condition manually — clear, rainy, or foggy.
"""