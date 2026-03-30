from core.speed_logic import get_speed_recommendation
from core.weather import validate_weather

def test_urban_clear():
    result = get_speed_recommendation("urban", "clear")
    assert result["recommended_speed_kmph"] == 50

def test_highway_clear():
    result = get_speed_recommendation("highway", "clear")
    assert result["recommended_speed_kmph"] == 120

def test_urban_rainy():
    result = get_speed_recommendation("urban", "rainy")
    assert result["recommended_speed_kmph"] == 35

def test_weather_validation():
    assert validate_weather("RAINY") == "rainy"
    assert validate_weather("invalid") == "clear"