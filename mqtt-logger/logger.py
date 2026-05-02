import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

import argparse
import socket
import uuid
from datetime import datetime

import logging
from logging.handlers import TimedRotatingFileHandler

# -----------------------
# ARGPARSE
# -----------------------
parser = argparse.ArgumentParser(description="MQTT Door Logger (v2 + log rotation)")

parser.add_argument("--broker", required=True, help="MQTT broker host/IP")
parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")

parser.add_argument("--user", help="MQTT username")
parser.add_argument("--password", help="MQTT password")

parser.add_argument("--state-topic", default="home/door/state")
parser.add_argument("--status-topic", default="home/door/status")

parser.add_argument("--log-file", default="door.log", help="Base log file name")

parser.add_argument("--client-id", help="Override MQTT client ID")

args = parser.parse_args()

# -----------------------
# UNIQUE CLIENT ID
# -----------------------
if args.client_id:
    client_id = args.client_id
else:
    hostname = socket.gethostname()
    random_suffix = uuid.uuid4().hex[:8]
    client_id = f"door_logger_{hostname}_{random_suffix}"

# -----------------------
# LOGGING SETUP (ROTATION)
# -----------------------
logger = logging.getLogger("door_logger")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    args.log_file,
    when="midnight",     # rotate daily
    interval=1,
    backupCount=30       # keep last 30 days
)

formatter = logging.Formatter(
    "[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

# also log to console
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)


def log(msg: str):
    logger.info(msg)

# -----------------------
# MQTT CLIENT (v2 API)
# -----------------------
client = mqtt.Client(
    client_id=client_id,
    callback_api_version=CallbackAPIVersion.VERSION2
)

if args.user:
    client.username_pw_set(args.user, args.password)

# -----------------------
# STATE TRACKING
# -----------------------
last_state = None
last_status = None

# -----------------------
# CALLBACKS (v2)
# -----------------------
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        log("Connected to MQTT broker")

        client.subscribe([
            (args.state_topic, 0),
            (args.status_topic, 0)
        ])
    else:
        log(f"Connection failed: {reason_code}")


def on_message(client, userdata, msg):
    global last_state, last_status

    payload = msg.payload.decode().strip()

    if msg.topic == args.state_topic:
        if payload != last_state:
            log(f"Door state changed → {payload}")
            last_state = payload

    elif msg.topic == args.status_topic:
        if payload != last_status:
            log(f"Device status → {payload}")
            last_status = payload


def on_disconnect(client, userdata, reason_code, properties):
    log(f"Disconnected from broker (reason={reason_code})")

# -----------------------
# REGISTER CALLBACKS
# -----------------------
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# -----------------------
# START
# -----------------------
log(f"Client ID: {client_id}")
log(f"Connecting to {args.broker}:{args.port}")

client.connect(args.broker, args.port, keepalive=60)
client.loop_forever()
