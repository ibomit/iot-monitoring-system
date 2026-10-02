from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.measurement import MeasurementResponse


class DeviceCreate(BaseModel):
    device_uid: str
    name: str
    location: str

class DeviceResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    device_uid: str
    name: str
    location: str
    created_at: datetime
    last_seen_at: datetime | None
    status: str

class DeviceDeleteResponse(BaseModel):
    success: bool
    message: str
    
class SensorDashboardResponse(BaseModel):
    sensor_uid: str
    name: str
    sensor_type: str
    latest_measurements: list[MeasurementResponse]

class DeviceDashboardResponse(BaseModel):
    device_uid: str
    name: str
    location: str
    last_seen_at: datetime | None
    status: str
    sensors: list[SensorDashboardResponse]