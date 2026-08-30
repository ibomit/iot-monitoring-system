#ifndef SENSOR_H
#define SENSOR_H

#include "../Measurement.h"

class Sensor {
    protected:
        const char* sensorUid;
        const char* name;
        const char* sensorType;

    public:
        Sensor(
            const char* sensorUid,
            const char* name,
            const char* sensorType
        )
            : sensorUid(sensorUid),
            name(name),
            sensorType(sensorType) {}

        virtual int read(
            Measurement* measurements
        ) = 0;

        const char* getSensorUid() const {
            return this->sensorUid;
        }
        const char* getName() const {
            return this->name;
        }
        const char* getSensorType() const{
            return this->sensorType;
        }

        virtual ~Sensor() = default;
};

#endif