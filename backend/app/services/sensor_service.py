from datetime import datetime

from sqlalchemy.orm import Session

from app import models
from app.exceptions import BadRequestError, NotFoundError
from app.schemas.sensor import SensorRegister
from app.services import measurement_service


def get_sensors(
    db: Session,
):
    return (
        db.query(models.Sensor)
        .all()
    )


def get_sensor_by_uid(
    db: Session,
    sensor_uid: str,
) -> models.Sensor | None:
    return (
        db.query(models.Sensor)
        .filter(
            models.Sensor.sensor_uid == sensor_uid
        )
        .first()
    )


def get_sensor_measurements(
    db: Session,
    sensor_id: int,
    limit: int = 100,
    start: datetime | None = None,
    end: datetime | None = None
):
    query = (
        db.query(models.Measurement)
        .filter(
            models.Measurement.sensor_id == sensor_id
        )
    )

    if start is not None:
        query = query.filter(
            models.Measurement.created_at >= start
        )
    
    if end is not None:
        query = query.filter(
            models.Measurement.created_at <= end
        )

    return (
        query
        .order_by(
            models.Measurement.created_at.desc()
        )
        .limit(limit)
        .all()
    )

def get_latest_measurements(
    db: Session,
    sensor_id: int,
):
    return measurement_service.get_latest_measurements_for_sensors(
        db,
        [sensor_id],
    )


def register_sensor(
    db: Session,
    data: SensorRegister,
):
    # Find device
    device = (
        db.query(models.Device)
        .filter(
            models.Device.device_uid == data.device_uid
        )
        .first()
    )

    if device is None:
        raise NotFoundError("Device not found")

    # Find sensor
    sensor = get_sensor_by_uid(
        db,
        data.sensor_uid,
    )

    # Sensor doesn't exist -> create it
    if sensor is None:
        sensor = models.Sensor(
            sensor_uid=data.sensor_uid,
            name=data.name,
            sensor_type=data.sensor_type,
            device_id=device.id,
        )

        db.add(sensor)
        db.commit()
        db.refresh(sensor)

        return sensor, True

    # Sensor exists but belongs to another device
    if sensor.device_id != device.id:
        raise BadRequestError(
            "Sensor UID already belongs to another device"
        )

    # Sensor already exists on this device
    return sensor, False