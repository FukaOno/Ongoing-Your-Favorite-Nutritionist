import os
import csv
import mysql.connector
from mysql.connector import Error

db_config = {
    "database" = "mealplan",
    "password" = "fuka1010",
    "user" = "root",
    "host" = "localhost"
    ""
}

def create_connection():
    return mysql.connector.connect(
        host = db_config["host"],
        database = db_config["database"],
        user = db_config["user"],
        host = db_config["host"],
        charset = 'utf8mb4', # 4 bytes(32 bits) in each character
        collation = 'utf8mb4_unicode_ci' #a set of rules that govern how data is sorted and compared in a database
    )

def parse_csv(file_name):
    script_direction = os.path.dirname(os.path.abspath(__file__))  # retrive the absolute direct path of this python file
    file_path = os.path.join(script_direction, file_name)




