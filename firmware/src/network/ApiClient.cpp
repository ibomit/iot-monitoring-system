#include "ApiClient.h"

#include <Arduino.h>
#include <HTTPClient.h>

ApiClient::ApiClient(
    const char* serverUrl,
    const char* deviceUid
){
    this->serverUrl = serverUrl;
    this->deviceUid = deviceUid;
}

void ApiClient::sendMeasurements(
    Measurement* measurements,
    int count
){
    String json =
        "{\"device_uid\":\"" +
        String(deviceUid) +
        "\",\"measurements\":[";

    for (int i = 0; i < count; i++) {

        json += "{";
        json += "\"metric\":\"" + measurements[i].metric + "\",";
        json += "\"value\":" + String(measurements[i].value, 1) + ",";
        json += "\"unit\":\"" + measurements[i].unit + "\"";
        json += "}";

        if (i < count - 1) {
            json += ",";
        }
    }

    json += "]}";

    HTTPClient http;

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(json);

    Serial.println();
    Serial.println("Sending measurements...");

    for(int i = 0; i < count; i++){
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