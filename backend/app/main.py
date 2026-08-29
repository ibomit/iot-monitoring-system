from fastapi import FastAPI
from pydantic import BaseModel

from app import models
from app.database import SessionLocal

app = FastAPI()

class MeasurementCreate(BaseModel):
    metric: str
    value: float
    unit: str
class MeasurementsCreate(BaseModel):
    device_uid: str
    measurements: list[MeasurementCreate]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/measurements")
def get_measurements():
    db = SessionLocal()
    try:
        measurements = db.query(models.Measurement).all()
        return measurements
    finally:
        db.close()

@app.post("/api/measurements")
def create_measurements(data: MeasurementsCreate):
    db = SessionLocal()

    try:
        device = (
            db.query(models.Device)
            .filter(models.Device.device_uid == data.device_uid)
            .first()
        )
        
        if device is None:
            return {
                "error": "Device not found"
            }
        saved_measurements = []

        for measurement in data.measurements:
            db_measurement = models.Measurement(
                device_id=device.id,
                metric=measurement.metric,
                value=measurement.value,
                unit=measurement.unit
            )
            db.add(db_measurement)
            saved_measurements.append(db_measurement)

        db.commit()

        return {
            "message": "Measurements saved",
            "count": len(saved_measurements)
        }
    finally:
        db.close()