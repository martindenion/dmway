import sqlite3
from sqlite3 import Error

class Database:
    """Cette classe comporte les méthodes nécessaire au stockage des données
    sur une base de données SQLite"""

    def __init__(self):
        """Identifie l'emplacement physique de la DB SQLite"""
        self.db_path = r"C:\Users\Martin\PycharmProjects\mdgateway\persistor\python_sqlite.db"  #but :memory: in Raspberry Pi
        self.conn_state = None
        self.sql_create_devices_table = """ CREATE TABLE IF NOT EXISTS devices (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        type text NOT NULL,
                                        ts integer,
                                        temperature real,
                                        humidity real,
                                        pressure real,
                                        luminosity real,
                                        sound
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
            self.conn_state = sqlite3.connect(self.db_path)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_table(self):
        """Création des tables gateway ou devices en fonction de la valeur de sql_table"""
        try:
            c = self.conn_state.cursor()
            c.execute(self.sql_create_devices_table)
            c.execute(self.sql_create_gateway_table)
        except Error as e:
            print(e)
