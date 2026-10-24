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

// The temperature of the room stays in this range
const float TEMPERATURE_MIN = 18.0;
const float TEMPERATURE_MAX = 27.0;

const float TEMPERATURE_BASELINE = 22.0;
const float HUMIDITY_BASELINE = 45.0;

// How strongly a reading is pulled toward the current temperature of the room
const float PULL = 0.05;

static float roundToTenth(float value) {
    return roundf(value * 10.0f) / 10.0f;
}

int FakeDHTSensor::read(
    Measurement* measurements
){
    // The room warms up and cools down slowly, over minutes and hours
    // (at most 0.04 °C per reading, in a random direction)
    temperatureTarget += random(-4, 5) / 100.0;
    temperatureTarget = constrain(temperatureTarget, TEMPERATURE_MIN, TEMPERATURE_MAX);

    // Warmer air holds relatively less humidity, so humidity moves the other way
    float humidityTarget =
        HUMIDITY_BASELINE - (temperatureTarget - TEMPERATURE_BASELINE) * 2.5;

    // The reading follows the room closely, with a little measurement noise
    // (up to 0.08 °C and 0.15 %), so it drifts instead of jumping
    temperature += random(-8, 9) / 100.0 + (temperatureTarget - temperature) * PULL;
    humidity += random(-15, 16) / 100.0 + (humidityTarget - humidity) * PULL;
    humidity = constrain(humidity, 30.0, 70.0);

    // The real DHT22 has a resolution of 0.1
    measurements[0] = {
        sensorUid,
        "temperature",
        roundToTenth(temperature),
        "celsius"
    };
    measurements[1] = {
        sensorUid,
        "humidity",
        roundToTenth(humidity),
        "percent"
    };
    return 2;
}