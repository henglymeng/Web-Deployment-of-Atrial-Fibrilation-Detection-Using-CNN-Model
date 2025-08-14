#include <WiFi.h>
#include <WebServer.h>

#define WIFI_STATUS 2    // Built-in LED
#define UNDETECTED_LED 0  // Green LED
#define DETECTED_LED 4   // RED or Yellow LED
#define BUZZER 5  // Buzzer

const char* ssid = "DESKTOP-796GSE4 0780";
const char* password = "tU8641^1";

WebServer server(80);

// DETECTED: turn ON LED, relay, buzzer
unsigned long buzzerStart = 0;
bool buzzerOn = false;

void handleDetected() {
  digitalWrite(DETECTED_LED, HIGH);
  digitalWrite(UNDETECTED_LED, LOW);
  digitalWrite(BUZZER, HIGH);
  buzzerStart = millis();
  buzzerOn = true;
  server.send(200, "text/plain", "DETECTED - Devices ON");
}

// UNDETECTED: turn OFF all devices
void handleUndetected() {
  digitalWrite(UNDETECTED_LED, HIGH);
  digitalWrite(DETECTED_LED, LOW);
  server.send(200, "text/plain", "UNDETECTED - Devices OFF");
}

void setup() {
  Serial.begin(115200);

  pinMode(WIFI_STATUS, OUTPUT);
  pinMode(UNDETECTED_LED, OUTPUT);
  pinMode(DETECTED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  digitalWrite(WIFI_STATUS, LOW);
  digitalWrite(DETECTED_LED, LOW);
  digitalWrite(UNDETECTED_LED, LOW);
  digitalWrite(BUZZER, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  digitalWrite(WIFI_STATUS, HIGH);
  delay(10);

  // Buzzer short beep after Wi-Fi connected
  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER, HIGH);
    delay(100);
    digitalWrite(BUZZER, LOW);
    delay(100);
  }

  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/DETECT", handleDetected);
  server.on("/detect", handleDetected);
  server.on("/UNDETECTED", handleUndetected);
  server.on("/undetected", handleUndetected);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();

  if (buzzerOn && (millis() - buzzerStart > 1000)) {
    digitalWrite(BUZZER, LOW);
    buzzerOn = false;
  }
}
