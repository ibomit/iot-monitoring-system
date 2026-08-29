#ifndef MEASUREMENT_H
#define MEASUREMENT_H

#include <Arduino.h>

struct Measurement {
    String metric;
    float value;
    String unit;
};

#endif