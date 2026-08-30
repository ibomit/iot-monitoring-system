from sqlalchemy.orm import Session

from app import models
from app.schemas.sensor import SensorRegister


def get_sensors(db: Session):

    return db.query(
        models.Sensor
    ).all()


def get_sensor_by_uid(
    db: Session,
    sensor_uid: str
):

    return (
        db.query(models.Sensor)
        .filter(
            models.Sensor.sensor_uid == sensor_uid
        )
        .first()
    )


def register_sensor(
    db: Session,
    data: SensorRegister
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
        return None, "device_not_found"

    # Find sensor
    sensor = get_sensor_by_uid(
        db,
        data.sensor_uid
    )

    # Sensor doesn't exist -> create it
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

        return sensor, "created"

    # Sensor exists but belongs to another device
    if sensor.device_id != device.id:

        return sensor, "wrong_device"

    # Sensor already exists on this device
    return sensor, "already_exists"