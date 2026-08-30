from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from app.dependencies import DbSession
from app.schemas.measurement import MeasurementResponse
from app.schemas.sensor import SensorRegister, SensorRegisterResponse, SensorResponse
from app.services import sensor_service

router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensors"]
)

@router.get(
    "/{sensor_uid}/measurements/latest",
    response_model=list[MeasurementResponse],
)
def get_latest_sensor_measurements(
    sensor_uid: str,
    db: DbSession,
):
    sensor = sensor_service.get_sensor_by_uid(
        db,
        sensor_uid,
    )

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found",
        )

    return sensor_service.get_latest_measurements(
        db,
        sensor.id,
    )


@router.get(
    "/{sensor_uid}/measurements",
    response_model=list[MeasurementResponse],
)
def get_sensor_measurements(
    sensor_uid: str,
    db: DbSession,
    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
    ),
    start: datetime | None = None,
    end: datetime | None = None
):
    if (
        start is not None
        and end is not None
        and start > end
    ):
        raise HTTPException(
            status_code=400,
            detail="Start time must be before end time"
        )
    sensor = sensor_service.get_sensor_by_uid(
        db,
        sensor_uid,
    )

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found",
        )

    return sensor_service.get_sensor_measurements(
        db,
        sensor.id,
        limit,
        start=start,
        end=end
    )

@router.post(
    "/register",
    response_model=SensorRegisterResponse
)
def register_sensor(
    data: SensorRegister,
    db: DbSession
):

    sensor, result = sensor_service.register_sensor(
        db,
        data
    )

    if result == "device_not_found":

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    if result == "wrong_device":

        raise HTTPException(
            status_code=400,
            detail=(
                "Sensor UID already belongs "
                "to another device"
            )
        )

    if result == "created":

        return {
            "message": "Sensor registered",
            "sensor_id": sensor.id
        }

    return {
        "message": "Sensor already registered",
        "sensor_id": sensor.id
    }


@router.get(
    "",
    response_model=list[SensorResponse]
)
def get_sensors(db: DbSession):

    return sensor_service.get_sensors(db)