from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.detect import router as detect_router

app = FastAPI(
    title="AI Smart Speed Regulator",
    description="YOLOv8 powered road type detection and speed recommendation system",
    version="1.0.0"
)

# Mount static files for UI
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(detect_router, prefix="/api", tags=["Detection"])

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/ping")
def ping():
    return {"message": "Smart Speed Regulator API is live"}


"""
main.py is the application entry point. 
It registers our detection router under `/api` prefix, serves the frontend UI from the static folder, 
and exposes a health check at `/ping`. 
This is standard production FastAPI architecture — same pattern used in real backend systems.
"""