from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models
from app.exceptions import ConflictError
from app.schemas.device import DeviceCreate
from app.services import measurement_service


def get_devices(db: Session):

    return db.query(
        models.Device
    ).all()


def get_device_by_uid(
    db: Session,
    device_uid: str
) -> models.Device:

    return (
        db.query(models.Device)
        .filter(
            models.Device.device_uid == device_uid
        )
        .first()
    )


def create_device(
    db: Session,
    data: DeviceCreate
):

    existing_device = get_device_by_uid(
        db,
        data.device_uid
    )

    if existing_device is not None:
        raise ConflictError("Device with this UID already exists.")

    device = models.Device(
        device_uid=data.device_uid,
        name=data.name,
        location=data.location
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device

def delete_device(
        db: Session,
        device: models.Device
) -> None:
    try:
        db.delete(device)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


def get_latest_device_measurements(
    db: Session,
    device_id: int,
):
    sensor_ids = [
        sensor_id
        for (sensor_id,) in db.query(models.Sensor.id).filter(
            models.Sensor.device_id == device_id
        )
    ]

    return measurement_service.get_latest_measurements_for_sensors(
        db,
        sensor_ids,
    )

def get_device_dashboard(
    db: Session,
    device: models.Device,
):
    measurements = measurement_service.get_latest_measurements_for_sensors(
        db,
        [sensor.id for sensor in device.sensors],
    )

    measurements_by_sensor = {}

    for measurement in measurements:
        if measurement.sensor_id not in measurements_by_sensor:
            measurements_by_sensor[measurement.sensor_id] = []

        measurements_by_sensor[measurement.sensor_id].append(
            measurement
        )

    sensors = []

    for sensor in device.sensors:
        sensors.append(
            {
                "sensor_uid": sensor.sensor_uid,
                "name": sensor.name,
                "sensor_type": sensor.sensor_type,
                "latest_measurements": measurements_by_sensor.get(
                    sensor.id,
                    [],
                ),
            }
        )

    return {
        "device_uid": device.device_uid,
        "name": device.name,
        "location": device.location,
        "last_seen_at": device.last_seen_at,
        "status": device.status,
        "sensors": sensors,
    }

