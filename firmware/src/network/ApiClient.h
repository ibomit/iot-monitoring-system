#ifndef API_CLIENT_H
#define API_CLIENT_H

#include "../Measurement.h"

class ApiClient {
    private:
        const char* serverUrl;
        const char* deviceUid;
    
    public:
        ApiClient(
            const char* serverUrl,
            const char* deviceUid
        );

        void sendMeasurements(
            Measurement* measurements,
            int count
        );
};

#endif