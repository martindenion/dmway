import sqlite3
import json
from sqlite3 import Error
from format.format import *


def number_question_marks(query):
    """
    Method that returns the number of question marks required for the query in the insert_device method
    :param query: str
    :return: list
    """
    marks_list = []
    for k in range(0, len(query)):
        marks_list.append('?')
    return marks_list

class Database:
    """This class includes the methods necessary for data storage on a SQLite database"""

    def __init__(self):
        """Identifies the physical location of the SQLite DB, the status of the connection to the SQLite database,
        and the devices and gateway tables"""
        self.db_path = r"C:\Users\Martin\PycharmProjects\mdgateway\persistor\python_sqlite.db"  #but :memory: in Raspberry Pi
        self.db_path_ram = ':memory:'
        self.db_path_sd = r"\home\pi\dmway\persistor\python_sqlite.db"
        self.sqlite_connection = None
        self.sql_create_devices_table = """ CREATE TABLE IF NOT EXISTS devices (
                                        id integer PRIMARY KEY,
                                        addr text NOT NULL,
                                        device text NOT NULL,
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
        """
        Procedure that allows to create the connection to the SQLite database
        :return:
        """
        print('Connecting to SQLite database ...')
        try:
            self.sqlite_connection = sqlite3.connect(self.db_path)
            print('Connected to SQLite database {}'.format(sqlite3.version))
        except Error as e:
            print(e)

    def create_table(self):
        """
        Procedure that allows to create devices and gateway tables
        :return:
        """
        try:
            cursor = self.sqlite_connection.cursor()
            cursor.execute(self.sql_create_devices_table)
            cursor.execute(self.sql_create_gateway_table)
        except Error as e:
            print(e)

    def insert_device(self, raw_json):
        """
        Procedure that allows the device to be registered in the devices table
        :param raw_json: str
        :return:
        """
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

    def delete_device(self, addr):
        """
        Procedure that allows the removal of a device from the devices table, having the MAC address specified
        in parameter
        :param addr: str
        :return:
        """
        try:
            sql_delete_query = "DELETE FROM devices WHERE addr = '" + addr + "'"
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sql_delete_query)
            self.sqlite_connection.commit()
        except sqlite3.Error as error:
            print("Failed to delete device from sqlite table", error)
        finally:
            if self.sqlite_connection:
                self.sqlite_connection.close()
                print("the sqlite connection is closed")

    def delete_all_devices(self):
        """
        Procedure that allows the removal of all devices from the table devices
        :return:
        """
        print('Cleaning SQLite database ...')
        try:
            sql_delete_query = "DELETE FROM devices;"
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sql_delete_query)
            print('SQLite database is now empty')
            self.sqlite_connection.commit()
        except sqlite3.Error as error:
            print("Failed to delete device from sqlite table", error)
        finally:
            if self.sqlite_connection:
                self.sqlite_connection.close()
                print("the sqlite connection is closed")

    def select_device(self, addr):
        """
        Method that selects the line of the devices table that has the MAC address specified in parameter and returns
        this line as a tuple
        :param addr: str
        :return:
        """
        try:
            sql_select_query = "SELECT * FROM devices WHERE addr = '" + addr + "'"
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sql_select_query)
            self.sqlite_connection.commit()
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as error:
            print("Failed to select device from sqlite table", error)
        finally:
            if self.sqlite_connection:
                self.sqlite_connection.close()
                print("the sqlite connection is closed")
        return rows[0]

    def select_all_devices(self):
        """
        Method that selects all lines in the device table with the MAC address specified in the parameter and returns
        a list of tuples, considering that each tple correspond to a line
        :return: list
        """
        row = []
        try:
            sql_select_query = "SELECT * FROM devices"
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sql_select_query)
            self.sqlite_connection.commit()
            rows = cursor.fetchall()
            for row in rows:
                print("{} selected from SQLite database".format(row))
        except sqlite3.Error as error:
            print("Failed to select device from sqlite table", error)
        finally:
            if self.sqlite_connection:
                self.sqlite_connection.close()
                print("the sqlite connection is closed")
        return rows