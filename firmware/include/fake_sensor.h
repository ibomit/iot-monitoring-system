#pragma once

#include "sensor.h"

class FakeSensor : public Sensor{
    public:
        SensorReading read() override;
};