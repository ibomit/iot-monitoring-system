#ifndef FAKE_DHT_SENSOR_H
#define FAKE_DHT_SENSOR_H

#include "Sensor.h"

class FakeDHTSensor : public Sensor {
    public:
    void read(
        Measurement* measurements,
        int& count
    ) override; 
};

#endif