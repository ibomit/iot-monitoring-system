import os

# Must be set before app modules are imported (security.py reads it at import)
os.environ["SECRET_KEY"] = "test-secret-key-only-for-pytest-0123456789abcdef"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401  (registers tables on Base.metadata)
from app.database import DATABASE_URL, Base, get_db
from app.main import app


def get_test_database_url() -> URL:
    """Return the URL of the test database.

    Uses TEST_DATABASE_URL if set, otherwise DATABASE_URL with "_test" appended
    to the database name. Refuses to run against anything not named "*_test",
    so the tests can never wipe the development database.
    """
    url = make_url(os.environ.get("TEST_DATABASE_URL") or DATABASE_URL)

    if not url.database.endswith("_test"):
        if os.environ.get("TEST_DATABASE_URL"):
            raise RuntimeError(
                "TEST_DATABASE_URL must point to a database whose name ends with '_test'"
            )
        url = url.set(database=f"{url.database}_test")

    return url


def ensure_database_exists(url: URL) -> None:
    admin_engine = create_engine(
        url.set(database="postgres"),
        isolation_level="AUTOCOMMIT",
    )

    with admin_engine.connect() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": url.database},
        ).scalar()

        if not exists:
            connection.execute(text(f'CREATE DATABASE "{url.database}"'))

    admin_engine.dispose()


@pytest.fixture(scope="session")
def engine():
    url = get_test_database_url()
    ensure_database_exists(url)

    test_engine = create_engine(url)
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    yield test_engine

    Base.metadata.drop_all(test_engine)
    test_engine.dispose()


@pytest.fixture
def session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(autouse=True)
def clean_tables(engine):
    yield

    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE measurements, sensors, devices, users "
                "RESTART IDENTITY CASCADE"
            )
        )


@pytest.fixture
def db(session_factory):
    """A session for asserting on database state directly."""
    session = session_factory()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(session_factory):
    def override_get_db():
        session = session_factory()

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def device(client):
    response = client.post(
        "/api/devices",
        json={
            "device_uid": "dev-1",
            "name": "Test device",
            "location": "Lab",
        },
    )
    assert response.status_code == 201

    return response.json()


@pytest.fixture
def sensor(client, device):
    response = client.post(
        "/api/sensors/register",
        json={
            "device_uid": device["device_uid"],
            "sensor_uid": "sensor-1",
            "name": "Test sensor",
            "sensor_type": "DHT",
        },
    )
    assert response.status_code == 200

    return {
        "device_uid": device["device_uid"],
        "sensor_uid": "sensor-1",
    }
