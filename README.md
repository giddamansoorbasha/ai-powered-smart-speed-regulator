# 🚦 AI-Powered Smart Speed Regulator

A real-time road safety system that detects road type using YOLOv8 
and recommends safe speed limits based on detected objects and weather conditions.

Built with FastAPI + YOLOv8 + OpenCV.

---

## 🎯 Features

- Real-time object detection using YOLOv8
- Detects pedestrians, cars, trucks, buses, bikes
- Classifies road type — urban, highway, rural, residential
- Recommends safe speed limits per road type
- Weather adaptation — reduces speed in rain/fog
- Pedestrian override — forces 20 kmph in residential zones
- Annotated image output with bounding boxes
- Clean REST API with Swagger docs

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Object Detection | YOLOv8 (Ultralytics) |
| Backend API | FastAPI |
| Image Processing | OpenCV |
| Frontend | HTML + JavaScript |
| Server | Uvicorn |

---

## 📁 Project Structure
```
smart-speed-regulator/
├── main.py                  # FastAPI entry point
├── requirements.txt         # Dependencies
├── core/
│   ├── detector.py          # YOLOv8 detection engine
│   ├── speed_logic.py       # Speed recommendation logic
│   └── weather.py           # Weather validation
├── routes/
│   └── detect.py            # API endpoints
├── static/
│   └── index.html           # Frontend UI
├── tests/
│   └── test_detect.py       # Unit tests
└── sample_images/           # Test images
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/smart-speed-regulator.git
cd smart-speed-regulator
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

### 5. Open browser
```
http://127.0.0.1:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/detect | Upload image + get speed recommendation |
| GET | /api/health | Health check |
| GET | /docs | Swagger UI |

### Sample Request
```bash
curl -X POST "http://localhost:8000/api/detect?weather=rainy" \
  -F "file=@road_image.jpg"
```

### Sample Response
```json
{
  "status": "success",
  "detection": {
    "road_type": "urban",
    "objects_detected": {
      "pedestrians": 5,
      "cars": 1,
      "trucks": 0,
      "buses": 0,
      "bikes": 0
    },
    "pedestrian_override": false
  },
  "speed_recommendation": {
    "recommended_speed_kmph": 35,
    "speed_range": "30–35 km/h",
    "reason": "Urban road under rainy conditions"
  },
  "weather": {
    "condition": "rainy",
    "description": "Rainy conditions — speed reduced by 15 kmph for safety."
  }
}
```

---

## 🏫 Academic Context

Project developed as part of TDPCL course — 4th Semester, CSE-AIML  
Jain University FET, Bangalore — 2026  
Guide: Dr. Shivkumar C

---

## 👨‍💻 Author

**Gidda Mansoor Basha**  
CSE-AIML | Jain University  
[GitHub](https://github.com/giddamansoorbasha)