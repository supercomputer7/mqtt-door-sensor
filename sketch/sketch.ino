#include <WiFi.h>
#include <PubSubClient.h>

// ===== USER CONFIG =====
const char* ssid = "WIFI SSID";
const char* password = "WIFI PASSWORD";

const char* mqtt_server = "MQTT_HOST";
const int   mqtt_port = 1883;
const char* mqtt_user = "USER";
const char* mqtt_pass = "PASS";

const char* client_id = "door_monitor";
const char* topic_status = "home/door/status";
const char* topic_gpio  = "home/door/state";

// GPIO pin
const int gpioPin = 4;

// ===== GLOBALS =====
WiFiClient espClient;
PubSubClient client(espClient);

int lastState = -1;
unsigned long lastReconnectAttempt = 0;

// ===== WIFI =====
void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// ===== MQTT RECONNECT =====
boolean reconnectMQTT() {
  Serial.print("Attempting MQTT connection...");

  // Last Will: send "offline" if device disconnects unexpectedly
  if (client.connect(
        client_id,
        mqtt_user,
        mqtt_pass,
        topic_status,
        1,            // QoS
        true,         // retain
        "offline"     // LWT message
      )) {

    Serial.println("connected");

    // Publish ONLINE status
    client.publish(topic_status, "online", true);

    return true;
  } else {
    Serial.print("failed, rc=");
    Serial.print(client.state());
    Serial.println(" try again later");
    return false;
  }
}

// ===== SETUP =====
void setup() {
  Serial.begin(115200);

  pinMode(gpioPin, INPUT_PULLUP); // change if needed

  setupWiFi();

  client.setServer(mqtt_server, mqtt_port);
}

// ===== LOOP =====
void loop() {

  // WiFi reconnect
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi lost. Reconnecting...");
    setupWiFi();
  }

  // MQTT reconnect
  if (!client.connected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt > 5000) {
      lastReconnectAttempt = now;
      if (reconnectMQTT()) {
        lastReconnectAttempt = 0;
      }
    }
  } else {
    client.loop();
  }

  // Read GPIO
  int currentState = digitalRead(gpioPin);

  if (currentState != lastState) {
    lastState = currentState;

    if (currentState == LOW) {
      client.publish(topic_gpio, "CLOSED", true);
      Serial.println("GPIO4: LOW");
    } else {
      client.publish(topic_gpio, "OPEN", true);
      Serial.println("GPIO4: HIGH");
    }
  }

  delay(100);
}