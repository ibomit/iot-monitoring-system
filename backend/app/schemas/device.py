from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
