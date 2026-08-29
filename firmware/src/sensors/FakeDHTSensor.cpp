#include "FakeDHTSensor.h"
#include <Arduino.h>

void FakeDHTSensor::read(
    Measurement* measurements,
    int& count
){
    float temperature = random(200, 300) / 10.0;
    float humidity = random(400, 500) / 10.0;

    measurements[0] = {
        "temperature",
        temperature,
        "celsius"
    };
    measurements[1] = {
        "humidity",
        humidity,
        "percent"
    };

    count = 2;
}