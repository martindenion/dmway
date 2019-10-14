import os
import time
import sys
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'iotplatform.int.cetic.be'
ACCESS_TOKEN = 'cmrtWotOUSysmsydspo4'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

#sensor_data = {'temperature': 0, 'humidity': 0}
sensor_data = {'device': 'device29'}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/gateway/connect', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

