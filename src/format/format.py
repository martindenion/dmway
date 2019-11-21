import json
import time


class Verification:
    """This class includes the methods necessary to check the format of the data received by the various sensors"""

    def __init__(self, topic, raw_json):
        self.topic = topic
        self.raw_json = raw_json
        self.json_schema = {}
        self.filtered_dict = {"device": "", "type": "", "ts": None, "values": {}}

    def set_json_schema_default(self, value):
        try:
            with open('schema.json') as json_schema:
                self.json_schema = self.json_file_to_dict(json_schema)
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except json.decoder.JSONDecodeError as wrong_json_format:
            print(wrong_json_format)

    def set_json_schema_custom(self, path):
        try:
            with open(path) as json_schema:
                self.json_schema = self.json_file_to_dict(json_schema)
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except json.decoder.JSONDecodeError as wrong_json_format:
            print(wrong_json_format)

    def json_string_to_dict(self, raw_json):
        """
        Method for converting a JSON message to a Python dictionary
        :param raw_json: str
        :return: dict
        """
        try:
            return json.loads(raw_json)
        except ValueError as value_error:
            print(value_error)

    def json_file_to_dict(self, raw_json):
        """
        Method for converting a JSON message to a Python dictionary
        :param raw_json: str
        :return: dict
        """
        try:
            return json.load(raw_json)
        except ValueError as value_error:
            print(value_error)

    def mapping_types(self, type_in_schema):
        switcher = {
            'int': int,
            'float': float,
            'str': str
        }
        return switcher.get(type_in_schema, int)

    def set_ts(self, splitted_topic):
        if not ("ts" in self.json_schema["topics"][splitted_topic]):
            self.filtered_dict['ts'] = int(round(time.time() * 1000))
        else:
            self.filtered_dict['ts'] = self.json_string_to_dict(self.raw_json)['ts']

    def filter_data(self):
        """
        Method that creates a Python dictionary that follows a format depending on the topic specified in argument
        The formats to follow are specified in schema.json file
        :return:
        """
        self.set_json_schema_default(None)
        raw_dict = self.json_string_to_dict(self.raw_json)
        splitted_topic = self.topic.split('/')
        # for schema_topics_key, schema_topics_value in json_schema["topics"].items():
        try:
            if splitted_topic[0] in self.json_schema["topics"].keys():
                try:
                    self.filtered_dict["device"] = raw_dict[self.json_schema["topics"][splitted_topic[0]]["device"]]
                    self.filtered_dict["type"] = raw_dict[self.json_schema["topics"][splitted_topic[0]]["type"]]
                    self.set_ts(splitted_topic[0])
                    for schema_values_key, schema_values_value in self.json_schema["topics"][splitted_topic[0]][
                        "values"].items():
                        if schema_values_key in raw_dict.keys():
                            for schema_type_element in \
                                    self.json_schema["topics"][splitted_topic[0]]["values"][schema_values_key]["type"]:
                                if isinstance(raw_dict[schema_values_key], self.mapping_types(schema_type_element)):
                                    self.filtered_dict["values"][schema_values_key] = raw_dict[schema_values_key]
                                    print(self.filtered_dict)
                except KeyError:
                    print("Error between : " + self.topic + " and : " + self.raw_json)
                except TypeError:
                    print("Missing fields in ", self.raw_json)
        except TypeError as type_error:
            print(type_error)
