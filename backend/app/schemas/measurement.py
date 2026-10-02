from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MeasurementCreate(BaseModel):

    sensor_uid: str = Field(min_length=1, max_length=100)
    metric: str = Field(min_length=1, max_length=100)
    value: float
    unit: str = Field(min_length=1, max_length=50)


class MeasurementsCreate(BaseModel):

    device_uid: str = Field(min_length=1, max_length=100)
    measurements: list[MeasurementCreate] = Field(max_length=100)


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