from fastapi import APIRouter, Query

from app.dependencies import DbSession
from app.schemas.measurement import (
    MeasurementResponse,
    MeasurementsCreate,
    MeasurementsCreateResponse,
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
    db: DbSession,
    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
    ),
):

    return measurement_service.get_measurements(
        db,
        limit,
    )


@router.post(
    "",
    response_model=MeasurementsCreateResponse
)
def create_measurements(
    data: MeasurementsCreate,
    db: DbSession
):

    measurements = measurement_service.create_measurements(
        db,
        data
    )

    return {
        "message": "Measurements saved",
        "count": len(measurements)
    }