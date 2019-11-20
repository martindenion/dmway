import json
import time


class Verification:
    """This class includes the methods necessary to check the format of the data received by the various sensors"""

    def __init__(self):
        """By default, the format is wrong"""
        self.success_keys = False
        self.success_values = False
        self.filtered_dict = {"device": "", "type": "", "values": {}}

    def json_to_dict(self, raw_json):
        """
        Method for converting a JSON message to a Python dictionary
        :param raw_json: str
        :return: dict
        """
        try:
            return json.loads(raw_json)
        except ValueError:
            print(raw_json + " correspond to a wrong JSON format")

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

    def modify_ts(self, raw_json):
        raw_dict = self.json_to_dict(raw_json)
        raw_dict['ts'] = int(round(time.time() * 1000))
        return json.dumps(raw_dict)

    def verify_keys(self, topic, raw_json):
        """
        Method that checks the format of the JSON message keys
        :param raw_json: str
        :return: bool
        """
        keys_list = self.get_keys(raw_json)
        all_keys_list = {
            "dev": {
                "device": "device",
                "type": "type",
                "values": ['mac', 'ts', 'temperature', 'humidity', 'pressure', 'luminosity', 'gas', 'loudness', 'iaq']
            },
            "zwave": {
                "device": "node_id",
                "type": "label",
                "values": ['energy', 'power']
            }
        }
        model_keys_list = []
        if topic.slipt('/')[1] in all_keys_list.keys():
            model_keys_list = all_keys_list[topic.slipt('/')[1]]

        if model_keys_list['device'] in keys_list and model_keys_list['type'] in keys_list:
            print('Verifying keys ...')
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
        print('Verifying values ...')
        for key, value in raw_dict.items():
            print('value : {}'.format(value))
            if (key == 'mac' or key == 'device' or key == 'type' or key == 'iaq') and (isinstance(value, str)):
                self.success_values = True
            elif isinstance(value, int) or isinstance(value, float) or isinstance(value, long):
                self.success_values = True
            elif isinstance(value, str):
                print("{} est de type str".format(value))
                self.success_values = False
            else:
                self.success_values = False
                break
        return self.success_values

    def json_schema_to_dict(self):
        with open('schema.json') as json_schema:
            return json.load(json_schema)

    def mapping_types(self, type_in_schema):
        switcher = {
            'int': int,
            'float': float,
            'str': str
        }
        return switcher.get(type_in_schema, int)

    def filter_data(self, topic, raw_json):
        v = Verification()
        topic_flag = False
        json_schema = v.json_schema_to_dict()
        raw_dict = self.json_to_dict(raw_json)
        splitted_topic = topic.split('/')
        # for schema_topics_key, schema_topics_value in json_schema["topics"].items():
        if splitted_topic[0] in json_schema["topics"].keys():
            try:
                self.filtered_dict["device"] = raw_dict[json_schema["topics"][splitted_topic[0]]["device"]]
                self.filtered_dict["type"] = raw_dict[json_schema["topics"][splitted_topic[0]]["type"]]
                print(self.filtered_dict)
                for schema_values_key, schema_values_value in json_schema["topics"][splitted_topic[0]][
                    "values"].items():
                    if schema_values_key in raw_dict.keys():
                        for schema_type_element in \
                                json_schema["topics"][splitted_topic[0]]["values"][schema_values_key]["type"]:
                            if isinstance(raw_dict[schema_values_key], self.mapping_types(schema_type_element)):
                                self.filtered_dict["values"][schema_values_key] = raw_dict[schema_values_key]
                                print(self.filtered_dict)
            except KeyError:
                print("Error between : " + topic + " and : " + raw_json)
            except TypeError:
                print("Missing fields in ", raw_json)