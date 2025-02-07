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
        cursor.execute("TRUNCATE TABLE FoodSources")  #Delete the existing vdata in the table
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

# insert_food_source()

def insert_foods():
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Disable checks
        cursor.execute("TRUNCATE TABLE Foods")  #Delete the existing vdata in the table
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  
        try:
            with open("cnf-fcen-csv/Foodname.csv", "r", encoding="ISO-8859-1") as foodfile:
                csv_reader = csv.reader(foodfile)
                next(csv_reader)  # Skip header

                row_count = 0
                success_count = 0
                for row in csv_reader:
                    row_count += 1
                    try:
                        # Pad missing columns
                        row += [''] * (10 - len(row))

                        # Parse data
                        food_id = int(row[0].strip()) if row[0].strip() else None
                        food_code = row[1].strip()
                        food_group_id = int(row[2].strip()) if row[2].strip() else None
                        food_source_id = int(row[3].strip()) if row[3].strip() else None
                        food_description = row[4].strip()
                        food_description_f = row[5].strip()

                        # Handle dates
                        try:
                            food_date_entry = datetime.strptime(row[6].strip(), "%Y-%m-%d").date()
                        except:
                            food_date_entry = None

                        food_date_pub = datetime.strptime(row[7].strip(), "%Y-%m-%d").date() if row[7].strip() else None
                        country_code = row[8].strip()
                        scientific_name = row[9].strip()

                        # Validate foreign keys
                        cursor.execute("SELECT FoodGroupID FROM FoodGroups WHERE FoodGroupID = %s", (food_group_id,))
                        if not cursor.fetchone():
                            print(f"Skipping row {row_count}: Invalid FoodGroupID {food_group_id}")
                            continue

                        # Insert into Foods
                        sql = """
                        INSERT INTO Foods 
                        (FoodID, FoodCode, FoodGroupID, FoodSourceID, FoodDescription, 
                        FoodDescriptionF, FoodDateOfEntry, FoodDateOfPublication, CountryCode, ScientificName)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        values = (
                            food_id,
                            food_code,
                            food_group_id,
                            food_source_id,
                            food_description,
                            food_description_f,
                            food_date_entry,
                            food_date_pub,
                            country_code,
                            scientific_name
                        )
                        cursor.execute(sql, values)
                        success_count += 1

                    except Exception as e:
                        print(f"Error in row {row_count}: {e}")
                        continue

                db_config.commit()
                print(f"Successfully inserted {success_count}/{row_count} rows!")

        except Exception as e:
            print(f"Fatal error: {e}")
            db_config.rollback()

    except Exception as e:
        print(f"Error: {e}")
        db_config.rollback()

# insert_foods()

#need to fix since there are many data that could not moved

def insert_measure_name():
    with open("cnf-fcen-csv/MEASURE NAME.csv", "r", encoding="ISO-8859-1") as fobj:
        csvreader = csv.reader(fobj)
        next(csvreader) #skip header row

        for row in csvreader:
            measure_id = int(row[0].strip()) if row[0].strip() else None
            # if len(row[0])>0:
                #food_group_id =row[0].strip()
            #else:
                #food_group_id =None
            measure_description = row[1].strip() 
            measure_description_f = row[2].strip()


            sql ="""
            INSERT INTO Measures
            (MeasureID, MeasureDescription, MeasureDescriptionF)
            VALUES (%s, %s, %s)
            """

            values = (
                measure_id,
                measure_description,
                measure_description_f
            )

            cursor.execute(sql, values)

    db_config.commit()
    print("Measure data inserted successfully")

# insert_measure_name()

#need to fix since there are many data that could not moved

def insert_conversion():
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Disable checks
        cursor.execute("TRUNCATE TABLE ConversionFactors")  #Delete the existing vdata in the table
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  
        try:
            with open("cnf-fcen-csv/CONVERSION FACTOR.csv", "r", encoding="ISO-8859-1") as fobj:
                csvreader = csv.reader(fobj)
                next(csvreader) #skip header row

                for row in csvreader:
                    food_id = int(row[0].strip()) if row[0].strip() else None
                    # if len(row[0])>0:
                        #food_group_id =row[0].strip()
                    #else:
                        #food_group_id =None
                    measure_id = int(row[1].strip()) if row[1].strip() else None
                    conversion_factor_value = row[2].strip()
                    conversion_factor_date_of_entry = datetime.strptime(row[3].strip(), "%Y-%m-%d").date()

                    #Foreign Key
                    cursor.execute("SELECT FoodGroupID FROM FoodGroups WHERE FoodGroupID = %s", (food_group_id,))
                        if not cursor.fetchone():
                            print(f"Skipping row {row_count}: Invalid FoodGroupID {food_group_id}")
                            continue

                    sql ="""
                    INSERT INTO ConversionFactors
                    (FoodID, MeasureID, ConversionFactorValue, ConvFactorDateOfEntry)
                    VALUES (%s, %s, %s, %s)
                    """

                    values = (
                        food_id,
                        measure_id,
                        conversion_factor_value,
                        conversion_factor_date_of_entry
                    )

                    cursor.execute(sql, values)
                    print("Conversion data inserted successfully")

        except Exception as e:
            print(f"Fatal error: {e}")
            db_config.rollback()

    except Exception as e:
        print(f"Error: {e}")
        db_config.rollback()
            db_config.commit()

insert_conversion()

#Fix the foreign key issue