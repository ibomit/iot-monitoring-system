#ifndef API_CLIENT_H
#define API_CLIENT_H

#include "../Measurement.h"
#include "../sensors/Sensor.h"

class ApiClient {
    private:
    
        const char* serverUrl;
        const char* deviceUid;
    
    public:

        ApiClient(
            const char* serverUrl,
            const char* deviceUid
        );

        void registerSensor(
            Sensor& sensor
        );

        void sendMeasurements(
            Measurement* measurements,
            int count
        );
};

#endif