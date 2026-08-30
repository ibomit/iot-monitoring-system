import random
import time

import httpx


BASE_URL = "http://localhost:8000"

DEVICE_UID = "simulator-001"

SENSORS = [
    {
        "sensor_uid": "sim-dht-001",
        "name": "Simulated DHT Sensor",
        "sensor_type": "DHT",
    },
    {
        "sensor_uid": "sim-distance-001",
        "name": "Simulated Distance Sensor",
        "sensor_type": "Distance",
    },
]


def register_sensors():
    for sensor in SENSORS:
        data = {
            "device_uid": DEVICE_UID,
            **sensor,
        }

        try:
            response = httpx.post(
                f"{BASE_URL}/api/sensors/register",
                json=data,
            )

            response.raise_for_status()

            print(
                f"Sensor registered: "
                f"{sensor['sensor_uid']}"
            )

        except httpx.RequestError as error:
            print(
                f"Could not register sensor: {error}"
            )


def generate_measurements():
    temperature = round(
        random.uniform(20, 30),
        2,
    )

    humidity = round(
        random.uniform(30, 70),
        2,
    )

    distance = round(
        random.uniform(100, 500),
        2,
    )

    return {
        "device_uid": DEVICE_UID,
        "measurements": [
            {
                "sensor_uid": "sim-dht-001",
                "metric": "temperature",
                "value": temperature,
                "unit": "celsius",
            },
            {
                "sensor_uid": "sim-dht-001",
                "metric": "humidity",
                "value": humidity,
                "unit": "percent",
            },
            {
                "sensor_uid": "sim-distance-001",
                "metric": "distance",
                "value": distance,
                "unit": "cm",
            },
        ],
    }


register_sensors()


while True:
    measurements = generate_measurements()

    try:
        response = httpx.post(
            f"{BASE_URL}/api/measurements",
            json=measurements,
        )

        response.raise_for_status()

        print("\nMeasurements sent:")
        print(measurements)

        print("\nResponse:")
        print(response.json())

    except httpx.RequestError as error:
        print(
            f"Could not connect to backend: {error}"
        )

    time.sleep(5)