from fastapi import APIRouter, HTTPException

from app.dependencies import DbSession
from app.schemas.sensor import (
    SensorRegister,
    SensorRegisterResponse,
    SensorResponse
)
from app.services import sensor_service


router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensors"]
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