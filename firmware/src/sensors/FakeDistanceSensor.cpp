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

// The HC-SR04 measures between about 2 and 400 cm
const float MIN_DISTANCE = 2.0;
const float MAX_DISTANCE = 400.0;

// The most the measured distance changes between two readings (cm)
const float MAX_STEP = 5.0;

int FakeDistanceSensor::read(
    Measurement* measurements
){
    // Now and then something moves in front of the sensor: a new target
    // between 50 and 250 cm. Most of the time the distance stays where it is.
    if (random(0, 100) < 2) {
        target = random(500, 2500) / 10.0;
    }

    // Move toward the target by at most MAX_STEP per reading
    distance += constrain(target - distance, -MAX_STEP, MAX_STEP);

    // Small measurement noise of about 0.3 cm
    float measured = distance + random(-3, 4) / 10.0;
    measured = constrain(measured, MIN_DISTANCE, MAX_DISTANCE);

    measurements[0] = {
        sensorUid,
        "distance",
        roundf(measured * 10.0f) / 10.0f,
        "cm"
    };

    return 1;
}