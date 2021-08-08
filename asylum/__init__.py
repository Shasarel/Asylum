import configparser
import sqlite3
import os

config = configparser.ConfigParser()
config.read(os.environ['ASYLUM_WEB_CONFIG'])

def create_sqlite3_connection():
    db_file = config['DATABASE']['Path']
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None
