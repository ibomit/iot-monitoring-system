import math
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

        except httpx.HTTPError as error:
            print(
                f"Could not register sensor: {error}"
            )


# The last values: every reading continues from the previous one, like a real
# sensor, instead of jumping to a new random value.
state = {
    "temperature": 22.0,
    "humidity": 45.0,
    "distance": 120.0,
    "distance_target": 120.0,
}

# A real day has 24 hours, so the "day" is compressed into 20 minutes to give
# the charts a visible shape. Warmer air is drier: humidity moves the opposite way.
DEMO_CYCLE_SECONDS = 20 * 60
PULL = 0.05  # how strongly a value is pulled back toward its slowly moving target


def generate_measurements():
    phase = math.sin(2 * math.pi * (time.time() % DEMO_CYCLE_SECONDS) / DEMO_CYCLE_SECONDS)

    temperature_target = 22.0 + 1.5 * phase
    humidity_target = 45.0 - 4.0 * phase

    # A small random step, pulled toward the target, so the value drifts
    state["temperature"] += (
        random.uniform(-0.1, 0.1)
        + (temperature_target - state["temperature"]) * PULL
    )
    state["humidity"] += (
        random.uniform(-0.15, 0.15)
        + (humidity_target - state["humidity"]) * PULL
    )
    state["humidity"] = min(70.0, max(30.0, state["humidity"]))

    # Now and then something moves in front of the sensor: a new target
    # distance. Otherwise the distance stays where it is.
    if random.random() < 0.02:
        state["distance_target"] = random.uniform(50, 250)
    difference = state["distance_target"] - state["distance"]
    state["distance"] += min(5.0, max(-5.0, difference))

    temperature = round(state["temperature"], 1)
    humidity = round(state["humidity"], 1)
    distance = round(
        min(400.0, max(2.0, state["distance"] + random.uniform(-0.3, 0.3))),
        1,
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

    except httpx.HTTPError as error:
        print(
            f"Backend request failed: {error}"
        )

    time.sleep(5)