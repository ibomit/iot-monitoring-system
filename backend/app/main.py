from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import models
from app.database import SessionLocal

app = FastAPI()


# Request Models
# =======================================================================================

class MeasurementCreate(BaseModel):
    sensor_uid: str
    metric: str
    value: float
    unit: str


class MeasurementsCreate(BaseModel):
    device_uid: str
    measurements: list[MeasurementCreate]


class SensorRegister(BaseModel):
    device_uid: str
    sensor_uid: str
    name: str
    sensor_type: str


# Health
# =======================================================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Sensors
# =======================================================================================

@app.post("/api/sensors/register")
def register_sensor(data: SensorRegister):

    db = SessionLocal()

    try:

        # Find device
        device = (
            db.query(models.Device)
            .filter(
                models.Device.device_uid == data.device_uid
            )
            .first()
        )

        if device is None:
            raise HTTPException(
                status_code=404,
                detail="Device not found"
            )

        # Check if sensor already exists
        sensor = (
            db.query(models.Sensor)
            .filter(
                models.Sensor.sensor_uid == data.sensor_uid
            )
            .first()
        )

        # Create sensor if it doesn't exist
        if sensor is None:

            sensor = models.Sensor(
                sensor_uid=data.sensor_uid,
                name=data.name,
                sensor_type=data.sensor_type,
                device_id=device.id
            )

            db.add(sensor)
            db.commit()
            db.refresh(sensor)

            return {
                "message": "Sensor registered",
                "sensor_id": sensor.id
            }

        # Sensor already exists
        if sensor.device_id != device.id:
            raise HTTPException(
                status_code=400,
                detail="Sensor UID already belongs to another device"
            )

        return {
            "message": "Sensor already registered",
            "sensor_id": sensor.id
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


@app.get("/api/sensors")
def get_sensors():

    db = SessionLocal()

    try:
        sensors = db.query(models.Sensor).all()

        return sensors

    finally:
        db.close()


# Measurements
# =======================================================================================

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

        # Find device
        device = (
            db.query(models.Device)
            .filter(
                models.Device.device_uid == data.device_uid
            )
            .first()
        )

        if device is None:
            raise HTTPException(
                status_code=404,
                detail="Device not found"
            )

        saved_measurements = []

        for measurement in data.measurements:

            # Find sensor
            sensor = (
                db.query(models.Sensor)
                .filter(
                    models.Sensor.sensor_uid
                    == measurement.sensor_uid
                )
                .first()
            )

            if sensor is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Sensor not found: {measurement.sensor_uid}"
                )

            # Verify sensor ownership
            if sensor.device_id != device.id:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Sensor {measurement.sensor_uid} "
                        "does not belong to this device"
                    )
                )

            db_measurement = models.Measurement(
                sensor_id=sensor.id,
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

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()