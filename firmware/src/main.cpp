#include <Arduino.h>
#include <WiFi.h>

#include "secrets.h"
#include "Measurement.h"
#include "sensors/FakeDHTSensor.h"
#include "network/ApiClient.h"

const char* SERVER_URL = "http://192.168.178.20:8000/api/measurements";

const char* DEVICE_UID = "esp32-001";

FakeDHTSensor sensor;

ApiClient apiClient(
    SERVER_URL,
    DEVICE_UID
);


void setup() {
    Serial.begin(115200);
    
    // Seed the Arduino random number generator
    randomSeed(esp_random());

    // Connect to Wi-Fi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    Serial.println("Connecting to Wi-Fi...");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("Wi-Fi connected!");
    Serial.print("ESP32 IP address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
 Measurement measurements[10];
    int count = 0;

    sensor.read(
        measurements,
        count
    );

    apiClient.sendMeasurements(
        measurements,
        count
    );

    delay(3000);
}