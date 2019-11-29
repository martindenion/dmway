import json
import signal
import threading
import paho.mqtt.client as mqtt
from src.format.format import Verification
import logging

from src.format.format import Verification


class SubThread(threading.Thread):
    def __init__(self, ip, topic, p):
        threading.Thread.__init__(self)
        self.ip = ip
        self.topic = topic
        self.client = None
        self.__p = p

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code " + str(rc) + " to a MQTT broker using this IP address : " + str(self.ip) + " and subscribing to this topic : " + str(self.topic))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.topic)

        # The callback for when a PUBLISH message is received from the server.

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        #logging.info(str(msg.topic) + " '" + str(payload) + "'" + str(len(payload)))
        v = Verification(payload, self.__p)
        v.start()

    def stop_running(self):
        self.client.disconnect()
        self.join()

    def run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.ip, 1883, keepalive=120)

        signal.signal(signal.SIGINT, self.stop_running())

        self.client.loop_forever()
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
