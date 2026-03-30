from ultralytics import YOLO
import cv2
import numpy as np
import base64

model = YOLO("yolov8n.pt")
print("✅ YOLOv8 model loaded successfully")

PEDESTRIAN_ID = 0
CAR_ID = 2
TRUCK_ID = 7
BUS_ID = 5
BIKE_ID = 1
MOTORCYCLE_ID = 3

def detect_objects(image_bytes: bytes) -> dict:

    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(img, verbose=True)[0]

    detected = {
        "pedestrians": 0,
        "cars": 0,
        "trucks": 0,
        "buses": 0,
        "bikes": 0,
    }

    # Draw boxes on image
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Pick color per object type
        if cls_id == PEDESTRIAN_ID:
            detected["pedestrians"] += 1
            color = (0, 0, 255)      # Red
            label = f"Person {conf:.0%}"
        elif cls_id == CAR_ID:
            detected["cars"] += 1
            color = (0, 255, 0)      # Green
            label = f"Car {conf:.0%}"
        elif cls_id == TRUCK_ID:
            detected["trucks"] += 1
            color = (255, 165, 0)    # Orange
            label = f"Truck {conf:.0%}"
        elif cls_id == BUS_ID:
            detected["buses"] += 1
            color = (255, 0, 255)    # Purple
            label = f"Bus {conf:.0%}"
        elif cls_id in [BIKE_ID, MOTORCYCLE_ID]:
            detected["bikes"] += 1
            color = (255, 255, 0)    # Yellow
            label = f"Bike {conf:.0%}"
        else:
            continue  # Skip irrelevant objects

        # Draw rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # Draw label background
        cv2.rectangle(img, (x1, y1 - 20), (x1 + len(label) * 9, y1), color, -1)

        # Draw label text
        cv2.putText(img, label, (x1 + 2, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Convert annotated image to base64 string
    _, buffer = cv2.imencode(".jpg", img)
    annotated_base64 = base64.b64encode(buffer).decode("utf-8")

    road_type = classify_road_type(detected)

    return {
        "detected_objects": detected,
        "road_type": road_type,
        "annotated_image": annotated_base64
    }


def classify_road_type(detected: dict) -> str:
    pedestrians = detected["pedestrians"]
    trucks = detected["trucks"]
    buses = detected["buses"]
    cars = detected["cars"]

    if pedestrians >= 3 and (cars + trucks + buses) <= 2:
        return "residential"
    if pedestrians >= 1 and (cars + buses) >= 1:
        return "urban"
    if (trucks + buses) >= 2 and pedestrians == 0:
        return "highway"
    if (cars + trucks + buses + pedestrians) <= 1:
        return "rural"

    return "urban"


"""
YOLOv8 is a state-of-the-art object detection model. 
We load it once at startup. For every image, it detects all objects and returns their class IDs. 
We count pedestrians, cars, trucks, buses — then use a rule-based classifier to determine road type. 
This mimics how a smart vehicle camera system would work in real life
"""