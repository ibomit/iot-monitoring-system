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

const unsigned long MEASUREMENT_INTERVAL_MS = 3000;
const unsigned long MAX_RETRY_DELAY_MS = 60000;
const int MAX_MEASUREMENTS_PER_BATCH = 10;

unsigned long nextMeasurementAt = 0;
unsigned long retryDelayMs = MEASUREMENT_INTERVAL_MS;
Measurement pendingMeasurements[MAX_MEASUREMENTS_PER_BATCH];
int pendingMeasurementCount = 0;

void connectToWiFi() {
    if (WiFi.status() == WL_CONNECTED) {
        return;
    }

    WiFi.disconnect();
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
}

unsigned long getRetryDelay(unsigned long currentDelay) {
    if (currentDelay >= MAX_RETRY_DELAY_MS / 2) {
        return MAX_RETRY_DELAY_MS;
    }

    return currentDelay * 2;
}

void setup() {
    Serial.begin(115200);
    
    // Seed the Arduino random number generator
    randomSeed(esp_random());

    connectToWiFi();
    
    // Register sensors

    apiClient.registerSensor(
        dhtSensor
    );
    
    apiClient.registerSensor(
        distanceSensor
    );
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("Wi-Fi connection lost. Reconnecting...");
        connectToWiFi();
        nextMeasurementAt = millis();
    }

    unsigned long now = millis();
    if (static_cast<long>(now - nextMeasurementAt) < 0) {
        delay(50);
        return;
    }

    if (pendingMeasurementCount == 0) {
        pendingMeasurementCount += dhtSensor.read(
            pendingMeasurements + pendingMeasurementCount
        );

        pendingMeasurementCount += distanceSensor.read(
            pendingMeasurements + pendingMeasurementCount
        );
    }

    if (pendingMeasurementCount == 0) {
        retryDelayMs = MEASUREMENT_INTERVAL_MS;
        nextMeasurementAt = millis() + retryDelayMs;
        return;
    }

    bool sent = apiClient.sendMeasurements(
        pendingMeasurements,
        pendingMeasurementCount
    );

    if (sent) {
        pendingMeasurementCount = 0;
        retryDelayMs = MEASUREMENT_INTERVAL_MS;
    } else {
        Serial.print("Retrying in ");
        Serial.print(retryDelayMs);
        Serial.println(" ms");
        retryDelayMs = getRetryDelay(retryDelayMs);
    }

    nextMeasurementAt = millis() + retryDelayMs;
}