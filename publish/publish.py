
#!/usr/bin/env python
import os
import time
import serial
import sys
import paho.mqtt.client as mqtt
import json
#send data to thingsboard
THINGSBOARD_HOST = 'iotplatform.int.cetic.be'
ACCESS_TOKEN = 'P1Wx6MO4SAgAr3nnqqYV'

# Data capture and upload interval in seconds. Less interval will eventually ha$
INTERVAL=10

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive inter$
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

ser = serial.Serial(
 port='/dev/ttyUSB0',
 baudrate = 115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0

try:
    while True:
        luminosity = ser.readline()
        # print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(temperature,$
        # sensor_data['temperature'] = temperature
        # sensor_data['humidity'] = humidity

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', luminosity)

        next_reading += INTERVAL
sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

