#include "FakeDistanceSensor.h"
#include <Arduino.h>

FakeDistanceSensor::FakeDistanceSensor(
    const char* sensorUid,
    const char* name
): Sensor(
    sensorUid,
    name,
    "Distance"
){}

int FakeDistanceSensor::read(
    Measurement* measurements
){
    float distance = random(1000, 5000) / 10.0;

    measurements[0] = {
        sensorUid,
        "distance",
        distance,
        "cm"
    };

    return 1;
}