#!/usr/bin/env python
import os
import time
import serial
import sys
import json

class Subscribe:
    def __init__(self):
        self.raw_json = '{"addr":"uneaddr","name":"uncapteur","type":"capteur","ts":1483228800000,"temperature":30,' \
                        '"humidity":50,"pressure":1015,"luminosity":10000,"sound":55}'
        self.interval = 10
        self.next_reading = time.time()
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

    def read_serial(self):
        try:
            while True:
                self.raw_json = self.ser.readline()
                self.next_reading += self.interval
                sleep_time = self.next_reading - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)
        except KeyboardInterrupt:
            pass