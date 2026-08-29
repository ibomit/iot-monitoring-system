#include <Arduino.h>
#include "fake_sensor.h"

SensorReading FakeSensor::read() {
    SensorReading reading; 

    reading.temperature = random(200, 300) / 10.0; 
    reading.humidity = random(200, 300) / 10.0;

    return reading;
};

