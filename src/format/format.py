import json
import time
import datetime


class Verification:
    """This class includes the methods necessary to check the format of the data received by the various sensors"""

    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.json_schema = {}
        self.filtered_dict = {"device": "", "type": "", "ts": None, "values": {}}
        self.standard_supported = []

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

    def set_ts(self, standard):
        if not ("ts" in self.json_schema["standard"][standard]):
            self.filtered_dict['ts'] = int(round(time.time() * 1000))
        else:
            self.filtered_dict['ts'] = self.json_string_to_dict(self.raw_json)['ts']

    def compare_rx_std(self):
        """
        Methods that compared keys in the JSON string received and keys in the different standards included in
        schema.json. This methods adds to standard_supported list the standards supported by the JSON received
        :return:
        """
        o = 0
        try:
            for keys, values in self.json_schema['standard'].items():
                for key in self.json_string_to_dict(self.raw_json).keys():
                    if key in values.keys():
                        o += 1
                if len(self.json_string_to_dict(self.raw_json)) == o:
                    print("Standard corresponds to the following standard :", keys)
                    self.standard_supported.append(keys)
                else:
                    print("Standard does not correspond to the following standard :", keys)
                o = 0
        except AttributeError as attribute_error:
            print(attribute_error, "(wrong JSON format)")
        except KeyError as key_error:
            print(key_error)

    def std_to_dmway(self):
        for key, value in self.json_schema['standard'][self.standard_supported[0]].items():
            if value == 'device':
                self.filtered_dict['device'] = self.json_string_to_dict(self.raw_json)[key]
            elif value == 'type':
                self.filtered_dict['type'] = self.json_string_to_dict(self.raw_json)[key]
            elif value == 'datetime':
                self.filtered_dict['ts'] = int(time.mktime(datetime.datetime.strptime(self.json_string_to_dict(self.raw_json)[key], "%Y-%m-%d %H:%M:%S").timetuple()))
            elif value == 'ts':
                self.filtered_dict['ts'] = self.json_string_to_dict(self.raw_json)[key]
            else:
                self.filtered_dict['ts'] = int(round(time.time() * 1000))

    def fld_to_dmway(self):
        if self.json_schema['fields'][self.standard_supported[0]]['values'] == "":
            for k, v in self.json_string_to_dict(self.raw_json).items():
                if k in self.json_schema['fields'][self.standard_supported[0]]['keys']:
                    self.filtered_dict['values'][k] = v
        else:
            for key, value in self.json_string_to_dict(self.raw_json).items():
                if isinstance(value, str):
                    if value.lower() in self.json_schema['fields'][self.standard_supported[0]]['keys']:
                        self.filtered_dict['values'][value] = self.json_string_to_dict(self.raw_json)[self.json_schema['fields'][self.standard_supported[0]]['values']]

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


    #def display_fields(self):
     #   for keys, values in self.json_schema["fields"][]