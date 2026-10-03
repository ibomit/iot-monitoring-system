from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorRegister(BaseModel):
    device_uid: str = Field(min_length=1, max_length=100)
    sensor_uid: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=100)
    sensor_type: str = Field(min_length=1, max_length=100)

class SensorResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    sensor_uid: str
    name: str
    sensor_type: str
    device_id: int
    created_at: datetime


class SensorRegisterResponse(BaseModel):
    message: str
    sensor_id: int