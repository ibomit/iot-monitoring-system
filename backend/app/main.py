from fastapi import FastAPI
from pydantic import BaseModel

from app import models
from app.database import Base, SessionLocal, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

class SensorReadingCreate(BaseModel):
    device_id: str
    temperature: float
    humidity: float

@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/api/readings")
def get_readings():
    db = SessionLocal()
    try:
        readings = db.query(models.SensorReading).all()
        
        return readings
        
    finally:
        db.close()

@app.post("/api/readings")
def create_reading(reading: SensorReadingCreate):
    db = SessionLocal()

    try:
        db_reading = models.SensorReading(
            device_id=reading.device_id,
            temperature=reading.temperature,
            humidity=reading.humidity
        )
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        
        return {
            "message": "Reading saved",
            "data": {
                "id": db_reading.id,
                "device_id": db_reading.device_id,
                "temperature": db_reading.temperature,
                "humidity": db_reading.humidity,
                "created_at": db_reading.created_at
            }
        }
    finally:
        db.close()