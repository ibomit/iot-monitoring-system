#include "FakeDHTSensor.h"
#include <Arduino.h>

FakeDHTSensor::FakeDHTSensor(
    const char* sensorUid,
    const char* name
)
    : Sensor(
        sensorUid,
        name,
        "DHT"
    ) {}

int FakeDHTSensor::read(
    Measurement* measurements
){
    float temperature = random(200, 300) / 10.0;
    float humidity = random(400, 500) / 10.0;

    measurements[0] = {
        sensorUid,
        "temperature",
        temperature,
        "celsius"
    };
    measurements[1] = {
        sensorUid,
        "humidity",
        humidity,
        "percent"
    };
    return 2;
}