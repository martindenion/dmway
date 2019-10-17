import os
import time
import sys
import paho.mqtt.client as mqtt
import json
from persistor.persist import *


class Publish:
    """This class includes the methods necessary to send data to Thingsboard while respecting its API"""

    def __init__(self):
        """Identifies the Thingsboard IP address and the access token to the gateway created on Thingsboard"""
        self.thingsboard_host = 'iotplatform.int.cetic.be'
        self.gnd_floor_gtw_access_token = 'untoken'
        self.fst_floor_gtw_access_token = 'cmrtWotOUSysmsydspo4'
        self.snd_floor_gtw_access_token = 'unautretoken'

    def create_device(self, raw_json, floor):
        """
        Method that allows to create a device on Thingsboard based on the gateway specified in parameter
        :param raw_json: str
        :param floor: int
        :return:
        """
        client = mqtt.Client()
        verif = Verification()
        floor_chosen = self.which_floor(floor)
        client.username_pw_set(floor_chosen)
        client.connect(self.thingsboard_host, 1883, 60)
        mac_address = verif.get_value(raw_json, "addr")
        raw_json = self.sqlite_to_telemetry(mac_address)
        client.loop_start()
        try:
            client.publish('v1/gateway/connect', raw_json, 1)
        except KeyboardInterrupt:
            pass
        client.loop_stop()
        client.disconnect()

    def create_devices(self):
        client = mqtt.Client()
        client.username_pw_set(self.fst_floor_gtw_access_token)
        client.connect(self.thingsboard_host, 1883, 60)
        raw_list = self.sqlite_to_connect_all_devices()
        client.loop_start()
        for dic in raw_list:
            try:
                client.publish('v1/gateway/connect', dic, 1)
                print('{} have been send to create device in Thingsboard'.format(dic))
            except KeyboardInterrupt:
                pass
        client.loop_stop()
        client.disconnect()

    def which_floor(self, floor):
        switcher = {
            0: self.gnd_floor_gtw_access_token,
            1: self.fst_floor_gtw_access_token,
            2: self.snd_floor_gtw_access_token,
        }
        return switcher.get(floor, self.gnd_floor_gtw_access_token)

    def send_telemetry(self, raw_json, floor):
        """
        Method that allows to send telemetry to Thingsboard based on the gateway specified in parameter
        :param raw_json: str
        :param floor: int
        :return:
        """
        client = mqtt.Client()
        verif = Verification()
        floor_chosen = self.which_floor(floor)
        client.username_pw_set(floor_chosen)
        client.connect(self.thingsboard_host, 1883, 60)
        mac_address = verif.get_value(raw_json, "addr")
        raw_json = self.sqlite_to_telemetry(mac_address)
        client.loop_start()
        try:
            client.publish('v1/gateway/telemetry', raw_json, 1)
        except KeyboardInterrupt:
            pass
        client.loop_stop()
        client.disconnect()

    def send_telemetry_all_devices(self):
        client = mqtt.Client()
        client.username_pw_set(self.fst_floor_gtw_access_token)
        client.connect(self.thingsboard_host, 1883, 60)
        raw_list = self.sqlite_to_telemetry_all_devices()
        client.loop_start()
        for dic in raw_list:
            try:
                client.publish('v1/gateway/telemetry', dic, 1)
                print('{} have been send to send telemetry to Thingsboard'.format(dic))
            except KeyboardInterrupt:
                pass
        client.loop_stop()
        client.disconnect()

    def sqlite_to_connect(self, addr):
        """
        Method that selects a line from the devices table and returns this data as a string respecting the
        Thingsboard API for connecting device
        :param addr: str
        :return: str
        """
        select = Database()
        select.create_connection()
        raw_dict = {}
        keys_list = ['device', 'type']
        raw_json = select.select_device(addr)
        i = 0
        j = 0
        for value in raw_json:
            if value is not None and 1 < i < 4:
                raw_dict[keys_list[j]] = value
                j += 1
            i += 1
        return json.dumps(raw_dict)

    def sqlite_to_connect_all_devices(self):
        select = Database()
        select.create_connection()
        raw_dict = {}
        keys_list = ['device', 'type']
        l = []
        raw_json = select.select_all_devices()
        i = 0
        j = 0
        for raw in raw_json:
            for value in raw:
                if value is not None and 1 < i < 4:
                    raw_dict[keys_list[j]] = value
                    j += 1
                i += 1
            l.append(json.dumps(raw_dict))
            i = 0
            j = 0
        return l

    def sqlite_to_telemetry(self, addr):
        """
        Method that selects a line from the devices table and returns this data as a string respecting the
        Thingsboard API for sending telemetry
        :param addr: str
        :return: str
        """
        select = Database()
        select.create_connection()
        raw_dict = {'ts': None, 'values': {}}
        keys_list = ['temperature', 'humidity', 'pressure', 'luminosity', 'sound']
        raw_json = select.select_device(addr)
        raw_dict['ts'] = raw_json[3]
        i = 0
        j = 0
        for value in raw_json:
            if value is not None and i > 4:
                raw_dict['values'][keys_list[j]] = value
                j += 1
            i += 1
        return '{\"' + raw_json[2] + '\": [' + json.dumps(raw_dict) + ']' + '}'

    def sqlite_to_telemetry_all_devices(self):
        select = Database()
        select.create_connection()
        raw_dict = {'ts': None, 'values': {}}
        keys_list = ['temperature', 'humidity', 'pressure', 'luminosity', 'sound']
        tuples_list = select.select_all_devices()
        i = 0
        j = 0
        l = []
        name = ""
        for tuples in tuples_list:
            for value in tuples:
                if value is not None:
                    if i == 2:
                        name = value
                    elif i == 4:
                        raw_dict['ts'] = value
                    elif i > 4:
                        raw_dict['values'][keys_list[j]] = value
                        j += 1
                i += 1
            l.append('{\"' + name + '\": [' +json.dumps(raw_dict) + ']' + '}')
            i = 0
            j = 0
        return l