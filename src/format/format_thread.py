import json
import threading

from src.format.format import Verification


class FormatThread(threading.Thread):
    def __init__(self, raw_json):
        self.raw_json = raw_json

    def run(self):
        v = Verification(self.raw_json)
        v.set_json_schema_default()
        v.compare_rx_std()
        v.check_value_to_send()
        v.rx_to_dmway()