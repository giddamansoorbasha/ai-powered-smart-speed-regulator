def get_speed_recommendation(road_type: str, weather: str = "clear") -> dict:
    
    speed_map = {
        "urban":       {"min": 30, "max": 50},
        "highway":     {"min": 80, "max": 120},
        "rural":       {"min": 20, "max": 40},
        "residential": {"min": 20, "max": 30},
        "unknown":     {"min": 20, "max": 40},
    }

    limits = speed_map.get(road_type, speed_map["unknown"])
    min_speed = limits["min"]
    max_speed = limits["max"]

    # Weather adjustment — reduce speed if bad weather
    weather_reduction = {
        "clear": 0,
        "rainy": 15,
        "foggy": 20,
    }

    reduction = weather_reduction.get(weather.lower(), 0)
    adjusted_max = max(min_speed, max_speed - reduction)

    return {
        "road_type": road_type,
        "weather": weather,
        "recommended_speed_kmph": adjusted_max,
        "speed_range": f"{min_speed}–{adjusted_max} km/h",
        "reason": f"{road_type.capitalize()} road under {weather} conditions"
    }


"""
Speed logic maps road type to safe speed range. 
If weather is rainy or foggy, 
it automatically reduces the maximum speed by 15–20 kmph. 
This mimics real traffic regulation rules used in smart city systems.
"""