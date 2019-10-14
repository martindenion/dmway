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

    def sqlite_to_send(self, id):
        select = Database()
        select.create_connection()
        raw_dict = {}
        keys_list = ['name', 'type', 'ts', 'temperature', 'humidity', 'pressure', 'luminosity', 'sound']
        raw_json = select.select_device(id)
        i = 0
        for value in raw_json:
            if value is not None:
                if i < 4:
                    raw_dict[keys_list[i]] = value[i+1]
        return raw_dict


