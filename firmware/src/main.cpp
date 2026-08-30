#include <Arduino.h>
#include <WiFi.h>

#include "secrets.h"
#include "Measurement.h"
#include "sensors/FakeDHTSensor.h"
#include "sensors/FakeDistanceSensor.h"
#include "network/ApiClient.h"

const char* SERVER_URL = 
    "http://192.168.178.20:8000";

const char* DEVICE_UID = 
    "esp32-001";

FakeDHTSensor dhtSensor(
    "fake-dht-001",
    "DHT Sensor"
);

FakeDistanceSensor distanceSensor(
    "fake_distance-001",
    "Distance Sensor"
);

ApiClient apiClient(
    SERVER_URL,
    DEVICE_UID
);


void setup() {
    Serial.begin(115200);
    
    // Seed the Arduino random number generator
    randomSeed(esp_random());

    // Connect to Wi-Fi
    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    Serial.println("Connecting to Wi-Fi...");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("Wi-Fi connected!");
    
    Serial.print("ESP32 IP address: ");
    Serial.println(WiFi.localIP());
    
    // Register sensors

    apiClient.registerSensor(
        dhtSensor
    );
    
    apiClient.registerSensor(
        distanceSensor
    );
}

void loop() {
    Measurement measurements[10];
    int count = 0;

    count += dhtSensor.read(
        measurements + count
    );

    count += distanceSensor.read(
        measurements + count
    );
    
    apiClient.sendMeasurements(
        measurements, 
        count
    );

    delay(3000);
}