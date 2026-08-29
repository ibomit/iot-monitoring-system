#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

#include "secrets.h"

const char* SERVER_URL = "http://192.168.178.20:8000/api/readings";

void send_fake_sensor_readings();

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
    send_fake_sensor_readings();

    // Send a reading every 3 seconds
    delay(3000);
}

void send_fake_sensor_readings() {
    // Generate fake sensor readings
    float random_temperature = random(200, 300) / 10.0;
    float random_humidity = random(400, 500) / 10.0;

    // Create JSON payload
    String json =
        "{\"device_id\":\"esp32-001\","
        "\"temperature\":" + String(random_temperature, 1) + ","
        "\"humidity\":" + String(random_humidity, 1) + "}";

    // Create HTTP client
    HTTPClient http;

    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    // Send POST request
    int httpResponseCode = http.POST(json);

    Serial.println();
    Serial.print("Temperature: ");
    Serial.println(random_temperature);

    Serial.print("Humidity: ");
    Serial.println(random_humidity);

    Serial.print("HTTP response code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
        Serial.println(http.getString());
    } else {
        Serial.print("HTTP error: ");
        Serial.println(http.errorToString(httpResponseCode));
    }

    // Close connection
    http.end();
}