#!/usr/bin/env python
import threading
import os
import time
#import serial
import sys
import json
import paho.mqtt.client as mqtt
import var


class SubThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.raw_json = '{"addr":"uneaddr","device":"fstcapteur","type":"capteur","ts":1483228800000,"temperature":30,' \
                        '"humidity":50,"pressure":1015,"luminosity":10000,"sound":55}'
        # self.interval = 10
        # self.next_reading = time.time()
        # self.ser = serial.Serial(
        #    port='/dev/ttyUSB0',
        #    baudrate=115200,
        #    parity=serial.PARITY_NONE,
        #    stopbits=serial.STOPBITS_ONE,
        #    bytesize=serial.EIGHTBITS,
        #    timeout=1
        #)
        self.broker_address = "localhost"
        self.client = None

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("/dev/+/data")

        # The callback for when a PUBLISH message is received from the server.

    def on_message(self, client, userdata, msg):
        print(msg.topic + " '" + str(msg.payload) + "'" + str(len(msg.payload)))
        var.raw_json = str(msg.payload)
        print("'" + str(msg.payload) + "'")

    def stop_running(self):
        self.client.disconnect()

    def run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.broker_address, 1883, 60)

        self.client.loop_forever()
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.


