from sqlalchemy.orm import Session

from app import models
from app.schemas.device import DeviceCreate


def get_devices(db: Session):

    return db.query(
        models.Device
    ).all()


def get_device_by_uid(
    db: Session,
    device_uid: str
):

    return (
        db.query(models.Device)
        .filter(
            models.Device.device_uid == device_uid
        )
        .first()
    )


def create_device(
    db: Session,
    data: DeviceCreate
):

    existing_device = get_device_by_uid(
        db,
        data.device_uid
    )

    if existing_device is not None:

        return None

    device = models.Device(
        device_uid=data.device_uid,
        name=data.name,
        location=data.location
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device