from fastapi import APIRouter, HTTPException, status

from app.dependencies import DbSession
from app.schemas.device import DeviceCreate, DeviceResponse
from app.services import device_service

router = APIRouter(
    prefix="/api/devices",
    tags=["Devices"]
)


@router.get(
    "",
    response_model=list[DeviceResponse]
)
def get_devices(db: DbSession):

    return device_service.get_devices(db)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_device(
    data: DeviceCreate,
    db: DbSession
):

    device = device_service.create_device(
        db,
        data
    )

    if device is None:

        raise HTTPException(
            status_code=400,
            detail="Device already exists"
        )

    return device


@router.get(
    "/{device_uid}",
    response_model=DeviceResponse
)
def get_device(
    device_uid: str,
    db: DbSession
):

    device = device_service.get_device_by_uid(
        db,
        device_uid
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return device