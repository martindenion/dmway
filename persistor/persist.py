import sqlite3
import json
from sqlite3 import Error
from format.format import *


def number_question_marks(query):
    marks_list = []
    for k in range(0, len(query)):
        marks_list.append('?')
    return marks_list

class Database:
    """Cette classe comporte les méthodes nécessaire au stockage des données
    sur une base de données SQLite"""

    def __init__(self):
        """Identifie l'emplacement physique de la DB SQLite"""
        self.db_path = r"C:\Users\Martin\PycharmProjects\mdgateway\persistor\python_sqlite.db"  #but :memory: in Raspberry Pi
        self.sqlite_connection = None
        self.sql_create_devices_table = """ CREATE TABLE IF NOT EXISTS devices (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        type text NOT NULL,
                                        ts integer,
                                        temperature real,
                                        humidity real,
                                        pressure real,
                                        luminosity real,
                                        sound real
                                    ); """
        self.sql_create_gateway_table = """CREATE TABLE IF NOT EXISTS gateway (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    temperature real,
                                    load real,
                                    ram real,
                                    ip text
                                );"""

    def create_connection(self):
        """Création de la connexion à la base de données SQLite"""
        try:
            self.sqlite_connection = sqlite3.connect(self.db_path)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_table(self):
        """Création des tables gateway ou devices en fonction de la valeur de sql_table"""
        try:
            cursor = self.sqlite_connection.cursor()
            cursor.execute(self.sql_create_devices_table)
            cursor.execute(self.sql_create_gateway_table)
        except Error as e:
            print(e)

    def insert_device(self, raw_json):
        """Enregistrement du device dans la table devices"""
        verif = Verification()
        query = verif.get_keys(raw_json)
        question_marks = number_question_marks(query)
        data = verif.get_values(raw_json)
        sql = ' INSERT INTO devices(' + ','.join(query) + ') VALUES (' + ','.join(question_marks) + ') '
        try:
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sql, data)
            print("{} insered in SQLite database".format(raw_json))
            self.sqlite_connection.commit()
        except sqlite3.Error as error:
            print("Failed to insert device in sqlite table", error)
        finally:
            if self.sqlite_connection:
                self.sqlite_connection.close()
                print("the sqlite connection is closed")

    def delete_device(self, id):
        """Suppression d'un device de la table devices"""
        try:
            sql_delete_query = 'DELETE FROM devices WHERE id = {}'.format(id)
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sql_delete_query)
            self.sqlite_connection.commit()
        except sqlite3.Error as error:
            print("Failed to delete device from sqlite table", error)
        finally:
            if self.sqlite_connection:
                self.sqlite_connection.close()
                print("the sqlite connection is closed")




