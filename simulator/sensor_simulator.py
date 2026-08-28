import random
import time

import httpx

while True:
    temperature = round(random.uniform(20, 30), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)

    reading = {
        "device_id": "sensor_1",
        "temperature": temperature,
        "humidity": humidity
    }

    try:
        response = httpx.post("http://localhost:8000/sensor_readings", json = reading)

        #TODO: Add Logger
        print("Sent")
        print(reading)

        print("\nResponse from server:")
        print(response.json())
    
    except httpx.RequestError as error:
        print(f"Could not connect to backend: {error}")

    time.sleep(5)
 