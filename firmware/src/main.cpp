#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "secrets.h"

const char* SERVER_URL = "http://192.168.178.20:8000/api/readings";

void setup() {
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("Connecting to Wi-Fi...");

  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Wi-Fi connected!");
  Serial.println("ESP32 IP address: ");
  Serial.println(WiFi.localIP());

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");

  String json = R"({
      "device_id": "esp32-001",
      "temperature": 23.5,
      "humidity": 45.0
  })";

  int httpResponseCode = http.POST(json);

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

void loop() {
}
