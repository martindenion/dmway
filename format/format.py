import json
import time


class Verification:
    """This class includes the methods necessary to check the format of the data received by the various sensors"""

    def __init__(self):
        """By default, the format is wrong"""
        self.success_keys = False
        self.success_values = False

    def json_to_dict(self, raw_json):
        """
        Method for converting a JSON message to a Python dictionary
        :param raw_json: str
        :return: dict
        """
        return json.loads(raw_json)

    def get_value(self, raw_json, key):
        """
        Method that returns the value of the JSON message corresponding to the key specified in the parameter
        :param raw_json: str
        :param key: str
        :return: dict
        """
        raw_dict = self.json_to_dict(raw_json)
        return raw_dict["{}".format(key)]

    def get_keys(self, raw_json):
        """
        Method that returns a list of all the keys of the JSON message
        :param raw_json: str
        :return: dict
        """
        raw_dict = self.json_to_dict(raw_json)
        keys_list = []
        for cle in raw_dict.keys():
            keys_list.append(cle)
        return keys_list

    def get_values(self, raw_json):
        """
        Method that returns a list of all the values of the JSON message
        :param raw_json: str
        :return: list
        """
        raw_dict = self.json_to_dict(raw_json)
        values_list = []
        for cle in raw_dict.values():
            values_list.append(cle)
        return values_list

    def set_ts(self, raw_json):
        ts = int(round(time.time() * 1000))
        raw_dict = self.json_to_dict(raw_json)
        raw_dict['ts'] = ts
        return json.dumps(raw_dict)

    def verify_keys(self, raw_json):
        """
        Method that checks the format of the JSON message keys
        :param raw_json: str
        :return: bool
        """
        keys_list = self.get_keys(raw_json)
        model_keys_list = ['addr', 'name', 'type', 'ts', 'temperature', 'humidity', 'pressure', 'luminosity', 'sound']
        if 'addr' in keys_list and 'name' in keys_list and 'type' in keys_list:
            for key in keys_list:
                print('key : {}'.format(key))
                if key in model_keys_list:
                    self.success_keys = True
                else:
                    self.success_keys = False
                    break
        else:
            self.success_keys = False
        return self.success_keys

    def verify_values(self, raw_json):
        """
        Method that checks the format of the JSON message values
        :param raw_json: str
        :return: bool
        """
        raw_dict = self.json_to_dict(raw_json)
        values_list = self.get_values(raw_json)
        for key, value in raw_dict.items():
            if (key == 'addr' or key == 'name' or key == 'type') and isinstance(value, str):
                self.success_values = True
            elif isinstance(value, int) or isinstance(value, float):
                self.success_values = True
            else:
                self.success_values = False
                break
        return self.success_values
