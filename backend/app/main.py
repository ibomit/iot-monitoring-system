import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app import models
from app.database import SessionLocal
from app.exceptions import (
    BadRequestError,
    ConflictError,
    DomainError,
    NotFoundError,
)
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
DOMAIN_ERROR_STATUS = {
    NotFoundError: 404,
    ConflictError: 409,
    BadRequestError: 400,
}


@app.exception_handler(DomainError)
async def handle_domain_error(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=DOMAIN_ERROR_STATUS.get(type(exc), 400),
        content={"detail": str(exc)},
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

