#ifndef FAKE_DHT_SENSOR_H
#define FAKE_DHT_SENSOR_H

#include "Sensor.h"

class FakeDHTSensor : public Sensor {
public:
    FakeDHTSensor(
        const char* sensorUid,
        const char* name    
    );

    int read(
        Measurement* measurements
    ) override;
};

#endif