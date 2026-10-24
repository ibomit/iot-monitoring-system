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

private:
    // The last values: every reading continues from the previous one
    float temperature = 22.0;
    float humidity = 45.0;

    // The temperature of the room, which changes slowly. The readings follow it.
    float temperatureTarget = 22.0;
};

#endif