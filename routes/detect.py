from fastapi import APIRouter, File, UploadFile, Query
from core.detector import detect_objects
from core.speed_logic import get_speed_recommendation
from core.weather import validate_weather, get_weather_description

router = APIRouter()


@router.post("/detect")
async def detect_and_recommend(
    file: UploadFile = File(...),
    weather: str = Query(default="clear", description="Weather: clear, rainy, foggy")
):
    """
    Upload a road image → get road type + speed recommendation.
    """

    # Step 1 — Read uploaded image
    image_bytes = await file.read()

    # Step 2 — Validate weather input
    validated_weather = validate_weather(weather)

    # Step 3 — Run YOLOv8 detection
    detection_result = detect_objects(image_bytes)

    # Step 4 — Get speed recommendation
    speed_result = get_speed_recommendation(
        road_type=detection_result["road_type"],
        weather=validated_weather
    )

    # Step 5 — Pedestrian override
    # If pedestrians detected in residential zone → force 20 kmph
    pedestrians = detection_result["detected_objects"]["pedestrians"]
    if pedestrians > 0 and detection_result["road_type"] == "residential":
        speed_result["recommended_speed_kmph"] = 20
        speed_result["speed_range"] = "20 km/h"
        speed_result["reason"] = "Pedestrian detected in residential zone — emergency speed override"

    # Step 6 — Build final response
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
        "weather": {
            "condition": validated_weather,
            "description": get_weather_description(validated_weather)
        },
        
        "annotated_image": detection_result["annotated_image"]
    }


@router.get("/health")
def health_check():
    return {"status": "API is running"}


"""
This is the core REST API endpoint. 
It accepts an image upload and weather condition. 
Internally it calls our detector, speed logic, and weather modules in sequence. 
The pedestrian override is a critical safety feature — if a pedestrian is detected in a residential zone, speed is forced to 20 kmph regardless of other conditions. 
This is how production safety systems work.
"""