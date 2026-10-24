"""Tests for the endpoints used by the ESP32 firmware and the simulator.

These pin the API contract: changing a status code or message here can break
devices in the field.
"""

from datetime import datetime, timedelta

from app import models


def measurement(sensor_uid, value=21.5, metric="temperature", unit="celsius"):
    return {
        "sensor_uid": sensor_uid,
        "metric": metric,
        "value": value,
        "unit": unit,
    }


def post_measurements(client, device_uid, measurements):
    return client.post(
        "/api/measurements",
        json={"device_uid": device_uid, "measurements": measurements},
    )


def register_sensor(client, device_uid, sensor_uid="sensor-1"):
    return client.post(
        "/api/sensors/register",
        json={
            "device_uid": device_uid,
            "sensor_uid": sensor_uid,
            "name": "Sensor",
            "sensor_type": "DHT",
        },
    )


# --- sensor registration ---------------------------------------------------


def test_register_sensor_is_idempotent(client, device):
    first = register_sensor(client, device["device_uid"])
    second = register_sensor(client, device["device_uid"])

    assert first.status_code == 200
    assert first.json()["message"] == "Sensor registered"
    assert second.status_code == 200
    assert second.json()["message"] == "Sensor already registered"
    assert second.json()["sensor_id"] == first.json()["sensor_id"]


def test_register_sensor_for_unknown_device_returns_404(client):
    response = register_sensor(client, "missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_register_sensor_owned_by_another_device_returns_400(client, device):
    client.post(
        "/api/devices",
        json={"device_uid": "dev-2", "name": "Second", "location": "Lab"},
    )
    register_sensor(client, device["device_uid"], "shared-sensor")

    response = register_sensor(client, "dev-2", "shared-sensor")

    assert response.status_code == 400
    assert response.json()["detail"] == "Sensor UID already belongs to another device"


# --- measurements ----------------------------------------------------------


def test_post_measurements_saves_and_marks_device_online(client, sensor):
    before = client.get(f"/api/devices/{sensor['device_uid']}").json()
    assert before["status"] == "unknown"

    response = post_measurements(
        client,
        sensor["device_uid"],
        [
            measurement(sensor["sensor_uid"], 21.5),
            measurement(sensor["sensor_uid"], 45.0, "humidity", "percent"),
        ],
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Measurements saved", "count": 2}

    after = client.get(f"/api/devices/{sensor['device_uid']}").json()
    assert after["status"] == "online"
    assert after["last_seen_at"] is not None


def test_post_measurements_for_unknown_device_returns_404(client):
    response = post_measurements(client, "missing", [measurement("sensor-1")])

    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_post_measurements_for_unknown_sensor_returns_404(client, device):
    response = post_measurements(client, device["device_uid"], [measurement("nope")])

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found: nope"


def test_post_measurements_for_sensor_of_other_device_returns_400(client, sensor):
    client.post(
        "/api/devices",
        json={"device_uid": "dev-2", "name": "Second", "location": "Lab"},
    )

    response = post_measurements(client, "dev-2", [measurement(sensor["sensor_uid"])])

    assert response.status_code == 400
    assert response.json()["detail"] == (
        f"Sensor {sensor['sensor_uid']} does not belong to this device"
    )


def test_post_measurements_is_all_or_nothing(client, sensor, db):
    from app import models

    response = post_measurements(
        client,
        sensor["device_uid"],
        [measurement(sensor["sensor_uid"]), measurement("nope")],
    )

    assert response.status_code == 404
    assert db.query(models.Measurement).count() == 0
    device = db.query(models.Device).one()
    assert device.last_seen_at is None


def test_post_measurements_rejects_oversized_input(client, sensor):
    too_many = [measurement(sensor["sensor_uid"])] * 101
    long_metric = measurement(sensor["sensor_uid"], metric="m" * 101)

    assert post_measurements(client, sensor["device_uid"], too_many).status_code == 422
    assert post_measurements(client, sensor["device_uid"], [long_metric]).status_code == 422


# --- reading data back -----------------------------------------------------


def test_latest_device_measurements_returns_newest_per_metric(client, sensor):
    for value in (1.0, 2.0, 3.0):
        post_measurements(
            client, sensor["device_uid"], [measurement(sensor["sensor_uid"], value)]
        )

    response = client.get(f"/api/devices/{sensor['device_uid']}/measurements/latest")

    assert response.status_code == 200
    assert [m["value"] for m in response.json()] == [3.0]


def test_latest_measurements_return_one_row_when_timestamps_tie(client, db, sensor):
    sensor_row = (
        db.query(models.Sensor)
        .filter(models.Sensor.sensor_uid == sensor["sensor_uid"])
        .one()
    )
    same_time = models.utcnow()

    for value in (1.0, 2.0):
        db.add(
            models.Measurement(
                sensor_id=sensor_row.id,
                metric="temperature",
                value=value,
                unit="celsius",
                created_at=same_time,
            )
        )
    db.commit()

    device_url = f"/api/devices/{sensor['device_uid']}"
    sensor_url = f"/api/sensors/{sensor['sensor_uid']}"

    device_latest = client.get(f"{device_url}/measurements/latest").json()
    sensor_latest = client.get(f"{sensor_url}/measurements/latest").json()
    dashboard = client.get(f"{device_url}/dashboard").json()

    # The row inserted last (highest id) wins the tie.
    assert [m["value"] for m in device_latest] == [2.0]
    assert [m["value"] for m in sensor_latest] == [2.0]
    assert [m["value"] for m in dashboard["sensors"][0]["latest_measurements"]] == [2.0]


def test_sensor_measurements_respect_limit_and_order(client, sensor):
    for value in (1.0, 2.0, 3.0):
        post_measurements(
            client, sensor["device_uid"], [measurement(sensor["sensor_uid"], value)]
        )

    response = client.get(
        f"/api/sensors/{sensor['sensor_uid']}/measurements", params={"limit": 2}
    )

    assert response.status_code == 200
    assert [m["value"] for m in response.json()] == [3.0, 2.0]


def test_sensor_measurements_reject_inverted_time_range(client, sensor):
    response = client.get(
        f"/api/sensors/{sensor['sensor_uid']}/measurements",
        params={"start": "2026-10-02T00:00:00Z", "end": "2026-10-01T00:00:00Z"},
    )

    assert response.status_code == 400


def test_list_measurements_is_limited(client, sensor):
    for value in (1.0, 2.0, 3.0):
        post_measurements(
            client, sensor["device_uid"], [measurement(sensor["sensor_uid"], value)]
        )

    assert len(client.get("/api/measurements", params={"limit": 2}).json()) == 2
    assert client.get("/api/measurements", params={"limit": 0}).status_code == 422
    assert client.get("/api/measurements", params={"limit": 5000}).status_code == 422


# --- measurement buckets (averages over time, used by the charts) ----------


def add_measurement(db, sensor_uid, metric, value, created_at):
    sensor_row = (
        db.query(models.Sensor)
        .filter(models.Sensor.sensor_uid == sensor_uid)
        .one()
    )
    db.add(
        models.Measurement(
            sensor_id=sensor_row.id,
            metric=metric,
            value=value,
            unit="u",
            created_at=created_at,
        )
    )
    db.commit()


def test_buckets_average_every_metric_per_time_bucket(client, db, sensor):
    base = models.utcnow().replace(microsecond=0) - timedelta(hours=1)
    uid = sensor["sensor_uid"]

    add_measurement(db, uid, "temperature", 10.0, base + timedelta(seconds=10))
    add_measurement(db, uid, "temperature", 20.0, base + timedelta(seconds=20))
    add_measurement(db, uid, "temperature", 30.0, base + timedelta(seconds=70))
    add_measurement(db, uid, "humidity", 50.0, base + timedelta(seconds=15))

    # 600 seconds with at most 10 points gives buckets of 60 seconds
    response = client.get(
        f"/api/sensors/{uid}/measurements/buckets",
        params={
            "start": base.isoformat(),
            "end": (base + timedelta(seconds=600)).isoformat(),
            "max_points": 10,
        },
    )

    assert response.status_code == 200
    buckets = [
        (
            item["metric"],
            datetime.fromisoformat(item["bucket_start"]),
            item["value"],
            item["count"],
        )
        for item in response.json()
    ]
    assert buckets == [
        ("humidity", base, 50.0, 1),
        ("temperature", base, 15.0, 2),
        ("temperature", base + timedelta(seconds=60), 30.0, 1),
    ]


def test_buckets_end_defaults_to_now(client, db, sensor):
    uid = sensor["sensor_uid"]
    add_measurement(
        db, uid, "temperature", 21.0, models.utcnow() - timedelta(minutes=5)
    )

    response = client.get(
        f"/api/sensors/{uid}/measurements/buckets",
        params={"start": (models.utcnow() - timedelta(hours=1)).isoformat()},
    )

    assert response.status_code == 200
    assert [item["value"] for item in response.json()] == [21.0]


def test_buckets_of_a_range_without_data_are_empty(client, sensor):
    response = client.get(
        f"/api/sensors/{sensor['sensor_uid']}/measurements/buckets",
        params={"start": (models.utcnow() - timedelta(hours=1)).isoformat()},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_buckets_reject_start_after_end(client, sensor):
    response = client.get(
        f"/api/sensors/{sensor['sensor_uid']}/measurements/buckets",
        params={"start": "2026-10-02T00:00:00Z", "end": "2026-10-01T00:00:00Z"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Start time must be before end time"


def test_buckets_for_unknown_sensor_return_404(client):
    response = client.get(
        "/api/sensors/missing/measurements/buckets",
        params={"start": "2026-10-01T00:00:00Z"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_buckets_validate_the_parameters(client, sensor):
    url = f"/api/sensors/{sensor['sensor_uid']}/measurements/buckets"

    assert client.get(url).status_code == 422
    assert (
        client.get(url, params={"start": "2026-10-01T00:00:00Z", "max_points": 5}).status_code
        == 422
    )
    assert (
        client.get(url, params={"start": "2026-10-01T00:00:00Z", "max_points": 5000}).status_code
        == 422
    )
