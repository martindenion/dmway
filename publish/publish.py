import os
import time
import sys
import paho.mqtt.client as mqtt
import json
from persistor.persist import *

class Publish:

    def __init__(self):
        self.thingsboard_host = 'iotplatform.int.cetic.be'
        self.gnd_floor_gtw_access_token = 'untoken'
        self.fst_floor_gtw_access_token = 'cmrtWotOUSysmsydspo4'
        self.snd_floot_gtw_access_token = 'unautretoken'

    def create_device(self, raw_json, floor):
        """Cette méthode permet de créer un device sur Thingsboard en fonction de la gateway indiquée"""
        client = mqtt.Client()
        floor_chosen = self.which_floor(floor)
        client.username_pw_set(floor_chosen)
        client.connect(self.thingsboard_host, 1883, 60)
        client.loop_start()
        try:
            client.publish('v1/gateway/connect', raw_json, 1)
        except KeyboardInterrupt:
            pass
        client.loop_stop()
        client.disconnect()

    def which_floor(self, floor):
        """Cette méthode renvoie le jeton d'accès correspondant à la passerelle de l'étage choisi"""
        switcher = {
            0: self.gnd_floor_gtw_access_token,
            1: self.fst_floor_gtw_access_token,
            2: self.snd_floot_gtw_access_token,
        }
        return switcher.get(floor, self.gnd_floor_gtw_access_token)

    def send_telemetry(self, raw_json, floor):
        """Cette méthode permet de créer un device sur Thingsboard, puis de lui envoyer les données récupérées
        par le Zolertia"""
        client = mqtt.Client()
        floor_chosen = self.which_floor(floor)
        client.username_pw_set(floor_chosen)
        client.connect(self.thingsboard_host, 1883, 60)
        client.loop_start()
        try:
            client.publish('v1/gateway/telemetry', raw_json, 1)
        except KeyboardInterrupt:
            pass
        client.loop_stop()
        client.disconnect()

    # else:
    #   raw_dict['values'][keys_list[i]] = value

    def sqlite_to_connect(self, id):
        select = Database()
        select.create_connection()
        raw_dict = {}
        keys_list = ['name', 'type']
        raw_json = select.select_device(id)
        i = 0
        j = 0
        for value in raw_json:
            if value is not None and 0 < i < 3:
                raw_dict[keys_list[j]] = value
                j += 1
            i += 1
        return json.dumps(raw_dict)

    def sqlite_to_telemetry(self, id):
        select = Database()
        select.create_connection()
        raw_dict = {'ts': 1483228801000, 'values' : {}}
        keys_list = ['temperature', 'humidity', 'pressure', 'luminosity', 'sound']
        raw_json = select.select_device(id)
        raw_dict['ts'] = raw_json[3]
        i = 0
        j = 0
        for value in raw_json:
            if value is not None and i > 3:
                raw_dict['values'][keys_list[j]] = value
                print(value)
                j += 1
            i += 1
        return '{\"' + raw_json[1] + "\": [" + json.dumps(raw_dict) + ']' + '}'

