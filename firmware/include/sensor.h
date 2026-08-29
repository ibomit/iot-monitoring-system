#pragma once

struct SensorReading{
    float temperature;
    float humidity;
};

class Sensor {

public:
    virtual SensorReading read() = 0;
    
    virtual ~Sensor() = default;
};