from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MeasurementCreate(BaseModel):

    sensor_uid: str
    metric: str
    value: float
    unit: str


class MeasurementsCreate(BaseModel):

    device_uid: str
    measurements: list[MeasurementCreate]


class MeasurementResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    sensor_id: int
    metric: str
    value: float
    unit: str
    created_at: datetime


class MeasurementsCreateResponse(BaseModel):

    message: str
    count: int