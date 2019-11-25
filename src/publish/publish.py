import paho.mqtt.client as mqtt
import json
import threading


class PubThread(threading.Thread):
    """This class includes the methods necessary to send data to Thingsboard while respecting its API"""

    def __init__(self, raw_connect, raw_telemetry):
        """Identifies the Thingsboard IP address and the access token to the gateway created on Thingsboard"""
        threading.Thread.__init__(self)
        self.gtw_access_token = 'cmrtWotOUSysmsydspo4'
        self.client = None
        self.thingsboard_host = "iotplatform.int.cetic.be"
        self.topic_connect = "v1/gateway/connect"
        self.topic_attributes = "v1/gateway/attributes"
        self.topic_telemetry = "v1/gateway/telemetry"
        self.raw_connect = raw_connect
        self.raw_telemetry = raw_telemetry

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK returned code", rc)
            self.client.loop_start()
            try:
                self.client.publish(self.topic_connect, self.raw_connect, qos=1)
                self.client.publish(self.topic_telemetry, self.raw_telemetry, qos=1)
            except KeyboardInterrupt:
                pass
            self.client.loop_stop()
            self.client.disconnect()
        else:
            print("Bad connection returned code", rc)

    def on_publish(self, client, obj, mid):
        print("mid: " + str(mid))

    def on_disconnect(client, userdata, rc):
        print("disconnecting reason  " + str(rc))

    def run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        print(self.raw_connect)
        print(self.raw_telemetry)
        self.client.username_pw_set(self.gtw_access_token)
        self.client.connect(self.thingsboard_host, port=1883, keepalive=60)

        self.client.loop_forever()