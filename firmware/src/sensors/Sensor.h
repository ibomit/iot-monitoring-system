#ifndef SENSOR_H
#define SENSOR_H

#include "../Measurement.h"

class Sensor {
    public:
    virtual ~Sensor() = default;
    virtual void read(
        Measurement* measurements,
        int& count
    ) = 0;
};

#endif