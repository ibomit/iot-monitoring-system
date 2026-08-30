from fastapi import APIRouter, HTTPException

from app.dependencies import DbSession

from app.schemas.measurement import (
    MeasurementResponse,
    MeasurementsCreate,
    MeasurementsCreateResponse
)

from app.services import measurement_service


router = APIRouter(
    prefix="/api/measurements",
    tags=["Measurements"]
)


@router.get(
    "",
    response_model=list[MeasurementResponse]
)
def get_measurements(
    db: DbSession
):

    return measurement_service.get_measurements(
        db
    )


@router.post(
    "",
    response_model=MeasurementsCreateResponse
)
def create_measurements(
    data: MeasurementsCreate,
    db: DbSession
):

    measurements, result = (
        measurement_service.create_measurements(
            db,
            data
        )
    )

    if result == "device_not_found":

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    if result.startswith("sensor_not_found:"):

        sensor_uid = result.split(
            ":",
            1
        )[1]

        raise HTTPException(
            status_code=404,
            detail=f"Sensor not found: {sensor_uid}"
        )

    if result.startswith("wrong_device:"):

        sensor_uid = result.split(
            ":",
            1
        )[1]

        raise HTTPException(
            status_code=400,
            detail=(
                f"Sensor {sensor_uid} "
                "does not belong to this device"
            )
        )

    return {
        "message": "Measurements saved",
        "count": len(measurements)
    }