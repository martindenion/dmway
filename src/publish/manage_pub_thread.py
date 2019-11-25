import json
import threading

from src.publish.publish import PubThread


class ManagPubThread(threading.Thread):
    def __init__(self, raw_dict):
        threading.Thread.__init__(self)
        self.raw_dict = raw_dict

    def run(self):
        if self.raw_dict != {}:
            self.raw_connect = {"device": self.raw_dict["device"], "type": str(self.raw_dict["type"])}
            self.raw_telemetry = {
                self.raw_dict["device"]: [
                    {
                        "ts": self.raw_dict["ts"],
                        "values": self.raw_dict["values"]
                    }
                ]
            }
            print(self.raw_connect)
            print(self.raw_telemetry)
            p = PubThread(json.dumps(self.raw_connect), json.dumps(self.raw_telemetry))
            p.start()
            p.join()