#pragma once

#include "sensor.h"

class FakeSensor : public Sensor{
    public:
        SensorReading read() override;
};

class FakeDHTSensor : public Sensor {
    public:
        void read() override;
}