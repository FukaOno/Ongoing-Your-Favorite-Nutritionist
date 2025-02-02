import os
import csv
from datetime import datetime
import mysql.connector
from mysql.connector import Error

db_config = mysql.connector.connect(
    database = "mealplan",
    password = "fuka1010",
    user = "root",
    host = "localhost"
)

cursor = db_config.cursor()

def insert_food_groups():
    with open("cnf-fcen-csv/foodgroup.csv", "r", encoding="latin-1") as fobj:
        csvreader = csv.reader(fobj)
        next(csvreader) #skip header row

        for row in csvreader:
            food_group_id = int(row[0].strip()) if row[0].strip() else None
            # if len(row[0])>0:
                #food_group_id =row[0].strip()
            #else:
                #food_group_id =None
            food_group_code = row[1].strip() 
            food_group_name = row[2].strip()
            food_group_name_f = row[3].strip()

            sql ="""
            INSERT INTO FoodGroups
            (FoodGroupID, FoodGroupCode, FoodGroupName, FoodGroupNameF)
            VALUES (%s, %s, %s, %s)
            """

            values = (
                food_group_id,
                food_group_code,
                food_group_name,
                food_group_name_f
            )

            cursor.execute(sql, values)

    db_config.commit()
    print("FoodGroups data inserted successfully")

insert_food_groups()


