from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SensorRegister(BaseModel):
    device_uid: str
    sensor_uid: str
    name: str
    sensor_type: str

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