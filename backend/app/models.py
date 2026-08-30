from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    device_uid: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    location: Mapped[str] = mapped_column(
        String(100)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )

    # measurements: Mapped[list["Measurement"]] = relationship(
    #     back_populates="device"
    # )
    sensors: Mapped[list["Sensor"]] = relationship(
        back_populates="device"
    )

class Sensor(Base):
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    
    sensor_uid: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(100)
    )
    sensor_type: Mapped[str] = mapped_column(
        String(100)
    )
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    device: Mapped["Device"] = relationship(
        back_populates="sensors"
    )

    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="sensor"
    )

class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        nullable=False,
    )

    metric: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )

    sensor: Mapped["Sensor"] = relationship(
        back_populates="measurements"
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )