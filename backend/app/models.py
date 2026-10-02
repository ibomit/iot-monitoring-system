from datetime import datetime, timedelta, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


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
        DateTime(timezone=True),
        default=utcnow,
    )

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    @property
    def status(self) -> str:
        if self.last_seen_at is None:
            return "unknown"

        if utcnow() - self.last_seen_at <= timedelta(minutes=2):
            return "online"

        return "offline"

    # measurements: Mapped[list["Measurement"]] = relationship(
    #     back_populates="device"
    # )
    sensors: Mapped[list["Sensor"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan",
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
        DateTime(timezone=True),
        default=utcnow
    )
    device: Mapped["Device"] = relationship(
        back_populates="sensors"
    )

    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="sensor",
        cascade="all, delete-orphan",
    )

class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = (
        Index(
            "ix_measurements_sensor_metric_created_at",
            "sensor_id",
            "metric",
            "created_at",
        ),
    )

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
        DateTime(timezone=True),
        default=utcnow,
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
        DateTime(timezone=True),
        default=utcnow,
        nullable=False
    )