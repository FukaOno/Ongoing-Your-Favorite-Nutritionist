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

# insert_food_groups()



def insert_food_source():
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Disable checks
        cursor.execute("TRUNCATE TABLE FoodSources")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  
        with open("cnf-fcen-csv/FOOD SOURCE.csv", "r", encoding = "ISO-8859-1") as foodsourcefile:
            read_csv= csv.reader(foodsourcefile)
            next(read_csv)

            for row in read_csv:
                food_source_id= int(row[0].strip()) if row[0].strip() else None
                food_source_code = row[1].strip()
                food_source_description = row[2].strip()
                food_source_description_f = row[3].strip()

                sql = """
                INSERT INTO FoodSources
                (FoodSourceID, FoodSourceCode, FoodSourceDescription, FoodSourceDescriptionF)
                VALUES (%s, %s, %s, %s)
                """

                values = (
                    food_source_id,
                    food_source_code,
                    food_source_description,
                    food_source_description_f
                )
                cursor.execute(sql, values)

            db_config.commit()
            print("Inserted Food Source!")
    except Exception as e:
        print(f"Error: {e}")
        db_config.rollback()

insert_food_source()

# def insert_food_name():
#     with open("cnf-fcen-csv/foodname.csv", "r", encode = "latin-1") as foodnamefile:
#         readcsv= csv.reader(foodnamefile)
#         next(readcsv)

#         for row in readcsv:
#             food_id= int(row[0].strip()) if row[0].strip() else None
#             food_code = row[1].strip
#             food_group_id = row[2].strip
#             food_source

#         sql = """
#         INSERT DATA 
        
#         """
