from sqlalchemy.orm import Session

from app import models
from app.schemas.measurement import MeasurementsCreate


def get_measurements(
    db: Session
):

    return (
        db.query(models.Measurement)
        .all()
    )


def create_measurements(
    db: Session,
    data: MeasurementsCreate
):

    try:

        # Find device
        device = (
            db.query(models.Device)
            .filter(
                models.Device.device_uid
                == data.device_uid
            )
            .first()
        )

        if device is None:

            return None, "device_not_found"

        # Get unique sensor UIDs from request
        sensor_uids = list({
            measurement.sensor_uid
            for measurement in data.measurements
        })

        # Get all sensors in one query
        sensors = (
            db.query(models.Sensor)
            .filter(
                models.Sensor.sensor_uid.in_(
                    sensor_uids
                )
            )
            .all()
        )

        # Create dictionary for fast lookup
        sensors_by_uid = {
            sensor.sensor_uid: sensor
            for sensor in sensors
        }

        saved_measurements = []

        # Process measurements
        for measurement in data.measurements:

            sensor = sensors_by_uid.get(
                measurement.sensor_uid
            )

            # Sensor not found
            if sensor is None:

                return (
                    None,
                    f"sensor_not_found:{measurement.sensor_uid}"
                )

            # Verify sensor belongs to device
            if sensor.device_id != device.id:

                return (
                    None,
                    f"wrong_device:{measurement.sensor_uid}"
                )

            db_measurement = models.Measurement(
                sensor_id=sensor.id,
                metric=measurement.metric,
                value=measurement.value,
                unit=measurement.unit
            )

            db.add(db_measurement)

            saved_measurements.append(
                db_measurement
            )

        # Save everything in one transaction
        db.commit()

        return saved_measurements, "created"

    except Exception:

        db.rollback()

        raise