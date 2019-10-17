#!/usr/bin/env python
import os
import time
import serial
import sys
import json
import paho.mqtt.client as mqtt

class Subscribe:
    def __init__(self):
        self.raw_json = '{"addr":"uneaddr","name":"fstcapteur","type":"capteur","ts":1483228800000,"temperature":30,' \
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

    def read_serial_to_mqtt(self):
        try:
            client = mqtt.Client()
            client.connect(self.broker_address)
            self.raw_json = client.subscribe("localhost/serial")
        except KeyboardInterrupt:
            pass
