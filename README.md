# MQTT Door Sensor (ESP32 + Python Logger)

A simple IoT project that detects when a door opens/closes using an ESP32 and publishes the state via MQTT.
A companion Python script subscribes to the MQTT topics and logs state changes with timestamps and log rotation.

---

## Components

### Hardware (what you will need)

* Arduino Nano ESP32 (or any ESP32 board)
* Magnetic reed switch (door sensor)
* A cable with at least two wires

### Software

* Arduino IDE with ESP32 support
* PubSubClient library
* Python 3
* `paho-mqtt` Python package

---

## ESP32 Firmware (Arduino Sketch)

Look in the [arduino build guide](ARDUINO_BUILD.md) for details on how to use this.

### Features

* Connects to WiFi
* Publishes door state (`open` / `closed`)
* Publishes availability (`online` / `offline`)
* Uses MQTT retained messages for state
* Uses Last Will and Testament (LWT)

---

## Python-based Logger

A Python script that:

* Subscribes to MQTT topics
* Logs only **state changes**
* Adds timestamps
* Rotates logs daily
* Keeps logs for **30 days**

---

### Logger Installation

Use a python `venv` as required, and then:

```bash
.venv/bin/pip install paho-mqtt
```

---

### Run!

Customize the parameters as required and then:
```bash
.venv/bin/python logger.py --broker MQTT_HOST --user MQTT_USER --password MQTT_PASS --state-topic home/door/state --status-topic home/door/status
```

### Install systemd service

Copy `mqtt-logger/systemd/door-mqtt-logger.service` to `/etc/systemd/system/door-mqtt-logger.service`,
customize the parameters.

Don't forget to do `systemctl daemon-reload` then enabling of the service.

---

### Log Output Example

```
[2026-05-02 14:00:01] Connected to MQTT broker
[2026-05-02 14:00:01] Device status → online
[2026-05-02 14:00:02] Door state changed → closed
[2026-05-02 14:05:10] Door state changed → open
[2026-05-02 14:10:22] Device status → offline
```

---

### Log Rotation

* Logs rotate **daily at midnight**
* Files are named like:

  ```
  door.log.2026-05-01
  ```
* Automatically deletes logs older than **30 days**

---

## Design Notes

### Why retained messages?

Retained messages ensure that subscribers immediately know the current door state after connecting.

### Why separate state and status?

* `state` = door position
* `status` = device availability

This prevents confusion between “door closed” and “device offline”.

---

## License

See [license](LICENSE) for more details.

---

## Acknowledgments

* PubSubClient (Arduino MQTT library)
* Eclipse Paho MQTT (Python client)

---
