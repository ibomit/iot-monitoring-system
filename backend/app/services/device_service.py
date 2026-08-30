from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.schemas.device import DeviceCreate


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

        return None

    device = models.Device(
        device_uid=data.device_uid,
        name=data.name,
        location=data.location
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device

def get_latest_device_measurements(
    db: Session,
    device_id: int,
):
    latest_measurements = (
        db.query(
            models.Sensor.id.label("sensor_id"),
            models.Measurement.metric,
            func.max(
                models.Measurement.created_at
            ).label("latest_created_at"),
        )
        .join(
            models.Measurement,
            models.Measurement.sensor_id == models.Sensor.id,
        )
        .filter(
            models.Sensor.device_id == device_id
        )
        .group_by(
            models.Sensor.id,
            models.Measurement.metric,
        )
        .subquery()
    )

    return (
        db.query(models.Measurement)
        .join(
            latest_measurements,
            (
                models.Measurement.sensor_id
                == latest_measurements.c.sensor_id
            )
            &
            (
                models.Measurement.metric
                == latest_measurements.c.metric
            )
            &
            (
                models.Measurement.created_at
                == latest_measurements.c.latest_created_at
            ),
        )
        .order_by(
            models.Measurement.sensor_id,
            models.Measurement.metric,
        )
        .all()
    )

def get_device_dashboard(
    db: Session,
    device: models.Device,
):
    latest_measurements = (
        db.query(
            models.Measurement.sensor_id.label("sensor_id"),
            models.Measurement.metric.label("metric"),
            func.max(
                models.Measurement.created_at
            ).label("latest_created_at"),
        )
        .join(
            models.Sensor,
            models.Measurement.sensor_id == models.Sensor.id,
        )
        .filter(
            models.Sensor.device_id == device.id,
        )
        .group_by(
            models.Measurement.sensor_id,
            models.Measurement.metric,
        )
        .subquery()
    )

    measurements = (
        db.query(models.Measurement)
        .join(
            latest_measurements,
            (
                models.Measurement.sensor_id
                == latest_measurements.c.sensor_id
            )
            &
            (
                models.Measurement.metric
                == latest_measurements.c.metric
            )
            &
            (
                models.Measurement.created_at
                == latest_measurements.c.latest_created_at
            ),
        )
        .all()
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
        "sensors": sensors,
    }

