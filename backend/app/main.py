from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import models
from app.database import SessionLocal
from app.routers import devices, sensors, measurements

tags_metadata = [
    {
        "name": "Health",
        "description": "API health and status endpoints."
    },
    {
        "name": "Devices",
        "description": "Manage IoT devices."
    },
    {
        "name": "Sensors",
        "description": "Register and manage sensors connected to devices."
    },
    {
        "name": "Measurements",
        "description": "Create and retrieve sensor measurements."
    }
]


app = FastAPI(
    title="IoT Monitoring System API",
    description="Backend API for managing IoT devices, sensors and measurements.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.include_router(devices.router)
app.include_router(sensors.router)
app.include_router(measurements.router)


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok"
    }

