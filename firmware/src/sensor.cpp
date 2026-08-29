#include <Arduino.h>
#include "sensor.h"

float get_temperature() {
    return random(200, 300) / 10.0;
}

float get_humidity() {
    return random(400, 500) / 10.0;
}