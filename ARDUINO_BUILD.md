# MQTT door sensor quick start guide

## Change Wi-Fi and MQTT credentials

Under `// ===== USER CONFIG =====` in the `sketch.ino`, you find these
credentials:

```c++
// ===== USER CONFIG =====
const char* ssid = "WIFI SSID";
const char* password = "WIFI PASSWORD";

const char* mqtt_server = "MQTT_HOST";
const int   mqtt_port = 1883;
const char* mqtt_user = "USER";
const char* mqtt_pass = "PASS";
```

Make sure to change them so you can connect to your network and MQTT
broker.

## Customize client ID, MQTT topics and GPIO input

Make sure to change those as required:
```c++
const char* client_id = "door_monitor";
const char* topic_status = "home/door/status";
const char* topic_gpio  = "home/door/state";

// GPIO pin
const int gpioPin = 4;
```

## Wiring 

By default the sketch uses GPIO4. This should be safe on most ESP32 boards,
but if change it, **make sure you pick a GPIO that is not a boot-strapping** one.

## Build using Arduino IDE

Make sure to open the sketch, and then select your board. I used Arduino
Nano ESP32, using the Espressif boards' package.

## Upload using DFU

Sadly, you might encounter a permissions' problem with uploading. You
can fix this with udev rules, but I found a quicker solution -

First, find your USB device. Make sure it's in DFU mode (for Arduino Nano
ESP32, double click RESET).
An `lsusb` output should look like this:
```
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 0bda:5650 Realtek Semiconductor Corp. Integrated Webcam_HD
Bus 001 Device 067: ID 2341:0070 Arduino SA ARDUINO_NANO_NORA
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
```

Then, simply allow anyone to access that device:
```sh
sudo chmod 777 /dev/bus/usb/001/067
```

Then compile and upload the sketch as usual from the IDE.
