import json
import threading

from src.subscribe.subscribe import SubThread


class ManagThread():
    def __init__(self):
        self.mqtt_broker = {}
        self.threads_list = []

    def set_json_schema_default(self):
        try:
            with open('mqtt_broker.json') as json_mqtt_broker:
                self.mqtt_broker = json.load(json_mqtt_broker)
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except json.decoder.JSONDecodeError as wrong_json_format:
            print(wrong_json_format)

    def create_sub_threads(self):
        for k, v in self.mqtt_broker['mqtt_broker'].items():
            t = SubThread(self.mqtt_broker['mqtt_broker'][k]['ip'], self.mqtt_broker['mqtt_broker'][k]['topic'])
            self.threads_list.append(t)

    def start_threads(self):
        for t in self.threads_list:
            t.start()

