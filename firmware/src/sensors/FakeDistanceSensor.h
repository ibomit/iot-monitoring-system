#ifndef FAKE_DISTANCE_SENSOR_H
#define FAKE_DISTANCE_SENSOR_H

#include "Sensor.h"

class FakeDistanceSensor : public Sensor {
public:
    FakeDistanceSensor(
        const char* sensorUid,
        const char* name
    );

    int read(
        Measurement* measurements
    ) override;
};

#endif