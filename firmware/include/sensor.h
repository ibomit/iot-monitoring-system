#pragma once

struct SensorReading{
    float temperature;
    float humidity;
};
struct Measurement {
    string metric;
    float value;
    string unit;
};


class Sensor {

public:
    virtual ~Sensor() = default;
    
    virtual void read(
        Measurement* measurements,
        int& count
    ) = 0
    
};