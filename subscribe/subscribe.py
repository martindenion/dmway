#!/usr/bin/env python
import os
import time
import serial
import sys
import json
import paho.mqtt.client as mqtt

class Subscribe:
    def __init__(self):
        self.raw_json = '{"addr":"uneaddr","device":"fstcapteur","type":"capteur","ts":1483228800000,"temperature":30,' \
                        '"humidity":50,"pressure":1015,"luminosity":10000,"sound":55}'
        # self.interval = 10
        # self.next_reading = time.time()
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.broker_address = "localhost"

    def on_connect(client, userdata, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("localhost")

    i = ""

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        global i
        i = str(msg.payload)

    def read_serial_to_mqtt(self):

        client = mqtt.Client()
        client.on_connect = self.on_connect()
        client.on_message = self.on_message()

        client.connect(self.broker_address, 1883, 60)
        self.raw_json = i
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        # client.loop_forever()
