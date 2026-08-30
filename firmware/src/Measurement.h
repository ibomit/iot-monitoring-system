#ifndef MEASUREMENT_H
#define MEASUREMENT_H

#include <Arduino.h>

struct Measurement {
    const char* sensorUid;
    const char* metric;
    float value;
    const char* unit;
};

#endif