#include "ApiClient.h"

#include <Arduino.h>
#include <HTTPClient.h>

const char* SENSORS_REGISTER_ENDPOINT =
    "/api/sensors/register";

const char* MEASUREMENTS_ENDPOINT =
    "/api/measurements";

ApiClient::ApiClient(
    const char* serverUrl,
    const char* deviceUid
)
    : serverUrl(serverUrl),
      deviceUid(deviceUid) {}

void ApiClient::registerSensor(
    Sensor& sensor
){
    HTTPClient http;
    String registerUrl=String(serverUrl) + SENSORS_REGISTER_ENDPOINT;

    http.begin(registerUrl);
    http.addHeader(
        "Content-Type",
        "application/json"
    );

    String json = "{";

    json += "\"device_uid\":\"";
    json += deviceUid;
    json += "\",";

    json += "\"sensor_uid\":\"";
    json += sensor.getSensorUid();
    json += "\",";

    json += "\"name\":\"";
    json += sensor.getName();
    json += "\",";

    json += "\"sensor_type\":\"";
    json += sensor.getSensorType();
    json += "\"";

    json += "}";


    Serial.println();
    Serial.println("Registering sensor...");
    Serial.println(json);


    int httpResponseCode =
        http.POST(json);


    Serial.print(
        "HTTP response code: "
    );

    Serial.println(
        httpResponseCode
    );


    if (httpResponseCode > 0) {
        Serial.println(
            http.getString()
        );
    } else {
        Serial.println(
            http.errorToString(
                httpResponseCode
            )
        );
    }


    http.end();
}
void ApiClient::sendMeasurements(
    Measurement* measurements,
    int count
){

    String json = "{";
    json += "\"device_uid\":\"";
    json += deviceUid;
    json += "\",";

    json += "\"measurements\":[";

    for (int i = 0; i < count; i++) {
        json += "{";

        json += "\"sensor_uid\":\"";
        json += measurements[i].sensorUid;
        json += "\",";

        json += "\"metric\":\"";
        json += measurements[i].metric;
        json += "\",";

        json += "\"value\":";
        json += String(measurements[i].value, 2);
        json += ",";

        json += "\"unit\":\"";
        json += measurements[i].unit;
        json += "\"";

        json += "}";

        if (i < count - 1) {
            json += ",";
        }
    }

    json += "]}";

    HTTPClient http;
    String measurementsUrl = String(serverUrl) + MEASUREMENTS_ENDPOINT;
    http.begin(measurementsUrl);
    http.addHeader(
        "Content-Type",
        "application/json"
    );


    int httpResponseCode = http.POST(json);

    Serial.println();
    Serial.println("Sending measurements...");

    for(int i = 0; i < count; i++){
        Serial.print(measurements[i].sensorUid);
        Serial.print(measurements[i].metric);
        Serial.print(": ");
        Serial.print(measurements[i].value);
        Serial.print(" ");
        Serial.println(measurements[i].unit);
    }
    Serial.print("HTTP response code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
        Serial.println(http.getString());
    } else {
        Serial.print("HTTP error: ");
        Serial.println(http.errorToString(httpResponseCode));
    }

    http.end();
}