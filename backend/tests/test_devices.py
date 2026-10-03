from datetime import datetime

from app import models


def test_create_device(client):
    response = client.post(
        "/api/devices",
        json={"device_uid": "dev-1", "name": "Name", "location": "Lab"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["device_uid"] == "dev-1"
    assert body["status"] == "unknown"
    assert body["last_seen_at"] is None


def test_create_duplicate_device_returns_409(client, device):
    response = client.post(
        "/api/devices",
        json={"device_uid": device["device_uid"], "name": "Other", "location": "Lab"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Device with this UID already exists."


def test_create_device_rejects_oversized_uid(client):
    response = client.post(
        "/api/devices",
        json={"device_uid": "x" * 101, "name": "Name", "location": "Lab"},
    )

    assert response.status_code == 422


def test_create_device_rejects_empty_name(client):
    response = client.post(
        "/api/devices",
        json={"device_uid": "dev-1", "name": "", "location": "Lab"},
    )

    assert response.status_code == 422


def test_get_unknown_device_returns_404(client):
    assert client.get("/api/devices/missing").status_code == 404
    assert client.get("/api/devices/missing/dashboard").status_code == 404
    assert client.get("/api/devices/missing/sensors").status_code == 404
    assert client.get("/api/devices/missing/measurements/latest").status_code == 404


def test_timestamps_are_timezone_aware(client, device):
    created_at = datetime.fromisoformat(device["created_at"])

    assert created_at.tzinfo is not None


def test_delete_device_cascades_to_sensors_and_measurements(client, sensor, db):
    client.post(
        "/api/measurements",
        json={
            "device_uid": sensor["device_uid"],
            "measurements": [
                {
                    "sensor_uid": sensor["sensor_uid"],
                    "metric": "temperature",
                    "value": 21.5,
                    "unit": "celsius",
                }
            ],
        },
    )
    assert db.query(models.Measurement).count() == 1

    response = client.delete(f"/api/devices/{sensor['device_uid']}")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert db.query(models.Device).count() == 0
    assert db.query(models.Sensor).count() == 0
    assert db.query(models.Measurement).count() == 0


def test_delete_unknown_device_returns_404(client):
    assert client.delete("/api/devices/missing").status_code == 404


def test_dashboard_lists_sensors_with_latest_measurements(client, sensor):
    for value in (20.0, 25.0):
        client.post(
            "/api/measurements",
            json={
                "device_uid": sensor["device_uid"],
                "measurements": [
                    {
                        "sensor_uid": sensor["sensor_uid"],
                        "metric": "temperature",
                        "value": value,
                        "unit": "celsius",
                    }
                ],
            },
        )

    response = client.get(f"/api/devices/{sensor['device_uid']}/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "online"
    assert len(body["sensors"]) == 1

    latest = body["sensors"][0]["latest_measurements"]
    assert [m["value"] for m in latest] == [25.0]
