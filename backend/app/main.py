import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import models
from app.database import SessionLocal
from app.routers import auth, devices, measurements, sensors

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


CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]


app = FastAPI(
    title="IoT Monitoring System API",
    description="Backend API for managing IoT devices, sensors and measurements.",
    version="1.0.0",
    openapi_tags=tags_metadata
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(devices.router)
app.include_router(sensors.router)
app.include_router(measurements.router)
app.include_router(auth.router)

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok"
    }

