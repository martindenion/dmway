import json
import time
import datetime


class Verification:
    """This class includes the methods necessary to check the format of the data received by the various sensors"""

    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.json_schema = {}
        self.filtered_dict = {}
        self.standard_supported = []
        self.value_to_send = False

    def set_json_schema_default(self):
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
        except KeyError:
            print('ERROR : First initialize schema.json as default schema')

    def rx_to_dmway(self):
        try:
            if self.value_to_send:
                self.filtered_dict = {"device": self.standard_supported[0] + 'defaultname', "type": self.standard_supported[0] + 'defaulttype', "ts": None, "values": {}}
                for key, value in self.json_schema['standard'][self.standard_supported[0]].items():
                    if value == 'device':
                        self.filtered_dict['device'] = self.standard_supported[0] + '_' + str(self.json_string_to_dict(self.raw_json)[key])
                    elif value == 'type':
                        self.filtered_dict['type'] = self.json_string_to_dict(self.raw_json)[key]
                    elif value == 'datetime':
                        self.filtered_dict['ts'] = int(time.mktime(datetime.datetime.strptime(self.json_string_to_dict(self.raw_json)[key], "%Y-%m-%d %H:%M:%S").timetuple()))
                    elif value == 'ts':
                        self.filtered_dict['ts'] = self.json_string_to_dict(self.raw_json)[key]
                    else:
                        self.filtered_dict['ts'] = int(round(time.time() * 1000))
                if self.json_schema['fields'][self.standard_supported[0]]['values'] == "":
                    for k, v in self.json_string_to_dict(self.raw_json).items():
                        if k in self.json_schema['fields'][self.standard_supported[0]]['keys']:
                            self.filtered_dict['values'][k] = v
                else:
                    for key, value in self.json_string_to_dict(self.raw_json).items():
                        if isinstance(value, str):
                            if value in self.json_schema['fields'][self.standard_supported[0]]['keys']:
                                self.filtered_dict['values'][value] = self.json_string_to_dict(self.raw_json)[
                                    self.json_schema['fields'][self.standard_supported[0]]['values']]
        except KeyError as key_error:
            print('ERROR : no', key_error, 'field in what dmway received')
            self.filtered_dict = {}

    def check_value_to_send(self):
        try:
            for k, v in self.json_string_to_dict(self.raw_json).items():
                if isinstance(k, str) or isinstance(v, str):
                    if (k in self.json_schema['fields'][self.standard_supported[0]]['keys']) or (v in self.json_schema['fields'][self.standard_supported[0]]['keys']):
                        self.value_to_send = True
        except AttributeError as attribute_error:
            print(attribute_error)
        except IndexError as index_error:
            print("ERROR :", index_error)

