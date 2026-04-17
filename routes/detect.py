from fastapi import APIRouter, File, UploadFile, Query
from core.detector import detect_objects
from core.speed_logic import get_speed_recommendation
from core.weather import validate_weather, get_weather_description
from core.live_weather import fetch_live_weather

router = APIRouter()


@router.post("/detect")
async def detect_and_recommend(
    file: UploadFile = File(...),
    weather: str = Query(default="clear", description="Manual: clear, rainy, foggy"),
    city: str = Query(default="", description="City name for live weather (optional)")
):
    """
    Upload a road image → get road type + speed recommendation.
    If city is provided → fetches live weather from OpenWeatherMap.
    Otherwise → uses manually selected weather condition.
    """

    # Step 1 — Read uploaded image
    image_bytes = await file.read()

    # Step 2 — Weather: live API or manual
    if city.strip():
        live = await fetch_live_weather(city.strip())
        validated_weather = live["condition"]
        weather_info = {
            "condition": validated_weather,
            "description": f"Live: {live['description']} in {live['city']}",
            "temperature_c": live["temperature_c"],
            "city": live["city"],
            "source": live["source"]
        }
    else:
        validated_weather = validate_weather(weather)
        weather_info = {
            "condition": validated_weather,
            "description": get_weather_description(validated_weather),
            "temperature_c": None,
            "city": None,
            "source": "manual"
        }

    # Step 3 — Run YOLOv8 detection
    detection_result = detect_objects(image_bytes)

    # Step 4 — Get speed recommendation
    speed_result = get_speed_recommendation(
        road_type=detection_result["road_type"],
        weather=validated_weather
    )

    # Step 5 — Pedestrian override
    pedestrians = detection_result["detected_objects"]["pedestrians"]
    if pedestrians > 0 and detection_result["road_type"] == "residential":
        speed_result["recommended_speed_kmph"] = 20
        speed_result["speed_range"] = "20 km/h"
        speed_result["reason"] = "Pedestrian detected in residential zone — emergency speed override"

    # Step 6 — Final response
    return {
        "status": "success",
        "detection": {
            "road_type": detection_result["road_type"],
            "objects_detected": detection_result["detected_objects"],
            "pedestrian_override": pedestrians > 0 and detection_result["road_type"] == "residential"
        },
        "speed_recommendation": {
            "recommended_speed_kmph": speed_result["recommended_speed_kmph"],
            "speed_range": speed_result["speed_range"],
            "reason": speed_result["reason"],
        },
        "weather": weather_info,
        "annotated_image": detection_result["annotated_image"]
    }


@router.get("/health")
def health_check():
    return {"status": "API is running"}