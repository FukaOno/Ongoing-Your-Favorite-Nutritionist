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
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE Measures")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
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

    except Exception as e:
        print(f"Error: {e}")
        db_config.rollback()

# insert_measure_name()

#need to fix since there are many data that could not moved

def insert_conversion():
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE ConversionFactors")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        with open("cnf-fcen-csv/CONVERSION FACTOR.csv", "r", encoding="ISO-8859-1") as fobj:
            csvreader = csv.reader(fobj)
            next(csvreader)  # Skip header

            success_count = 0
            error_count = 0

            for row in csvreader:
                try:
                    # Pad missing columns
                    row += [''] * (4 - len(row))

                    # Parse data
                    food_id = int(row[0].strip()) if row[0].strip() else None
                    measure_id = int(row[1].strip()) if row[1].strip() else None
                    conversion_factor_value = float(row[2].strip()) if row[2].strip() else None  # Convert to float

                    # Handle date (skip if invalid)
                    try:
                        conversion_date = datetime.strptime(row[3].strip(), "%Y-%m-%d").date()
                    except (ValueError, AttributeError):
                        print(f"Skipping row (invalid date): {row}")
                        error_count += 1
                        continue

                    # Validate foreign keys
                    cursor.execute("SELECT FoodID FROM Foods WHERE FoodID = %s", (food_id,))
                    if not cursor.fetchone():
                        print(f"Skipping row (invalid FoodID {food_id}): {row}")
                        error_count += 1
                        continue

                    cursor.execute("SELECT MeasureID FROM Measures WHERE MeasureID = %s", (measure_id,))
                    if not cursor.fetchone():
                        print(f"Skipping row (invalid MeasureID {measure_id}): {row}")
                        error_count += 1
                        continue

                    # Insert into ConversionFactors
                    sql = """
                    INSERT INTO ConversionFactors 
                    (FoodID, MeasureID, ConversionFactorValue, ConvFactorDateOfEntry)
                    VALUES (%s, %s, %s, %s)
                    """
                    values = (
                        food_id,
                        measure_id,
                        conversion_factor_value,
                        conversion_date
                    )
                    cursor.execute(sql, values)
                    success_count += 1

                except Exception as e:
                    print(f"Error in row {row}: {e}")
                    error_count += 1
                    continue

            db_config.commit()
            print(f"Inserted {success_count} rows. Errors: {error_count}")

    except Exception as e:
        print(f"Fatal error: {e}")
        db_config.rollback()
# insert_conversion()

def insert_nutrients_name():
    with open ("cnf-fcen-csv/NUTRIENT NAME.csv", "r", encoding="ISO-8859-1") as fobj:
        csvread= csv.reader(fobj)
        next(csvread)

        for row in csvread:
            nutrient_id = int(row[0].strip()) if row[0].strip() else None
            nutrient_code = int(row[1].strip()) if row[1].strip() else None
            nutrient_symbol = row[2].strip()
            nutrient_nunit = row[3].strip()
            nutrient_name = row[4].strip()
            nutrient_name_f = row[5].strip()
            tag_name = row[6].strip()
            nutrient_decimal = row[7].strip()

            sql ="""
            INSERT INTO Nutrients (
            NutrientID, NutrientCode, NutrientSymbol, NutrientUnit, NutrientName, NutrientNameF, Tagname, NutrientDecimals
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                nutrient_id,
                nutrient_code,
                nutrient_symbol,
                nutrient_nunit,
                nutrient_name,
                nutrient_name_f,
                tag_name,
                nutrient_decimal
            )

            cursor.execute(sql, values)

    db_config.commit()
    print("Nutrients data inserted successfully")

# insert_nutrients_name()

def insert_nutrients_sources():
    with open ("cnf-fcen-csv/NUTRIENT SOURCE.csv", "r", encoding="ISO-8859-1") as fobj:
        csvread= csv.reader(fobj)
        next(csvread)

        for row in csvread:
            nutrient_source_id = int(row[0].strip()) if row[0].strip() else None
            nutrient_source_code = int(row[1].strip()) if row[1].strip() else None
            nutrient_source_desc = row[2].strip()
            nutrient_source_desc_f = row[3].strip()

            sql ="""
            INSERT INTO NutrientSources (
            NutrientSourceID, NutrientSourceCode, NutrientSourceDescription, NutrientSourceDescriptionF
            )
            VALUES (%s, %s, %s, %s)
            """

            values = (
                nutrient_source_id ,
                nutrient_source_code,
                nutrient_source_desc,
                nutrient_source_desc_f
            )

            cursor.execute(sql, values)

        db_config.commit()
        print("NutrientsSources inserted successfully")

# insert_nutrients_sources()


def insert_nutrients_amount():
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE NutrientAmounts")  # Corrected name
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        with open("cnf-fcen-csv/NUTRIENT AMOUNT.csv", "r", encoding="ISO-8859-1") as fobj:
            csvread = csv.reader(fobj)
            next(csvread)  # Skip header

            error_count = 0
            success_count = 0

            for row in csvread:
                try:
                    # Pad missing columns
                    row += [''] * (7 - len(row))

                    # Parse data
                    food_id = int(row[0].strip()) if row[0].strip() else None
                    nutrient_id = int(row[1].strip()) if row[1].strip() else None
                    nutrient_value = float(row[2].strip()) if row[2].strip() else None  # Convert to float
                    standard_error = float(row[3].strip()) if row[3].strip() else None
                    num_observation = int(row[4].strip()) if row[4].strip() else None
                    nutrient_source_id = int(row[5].strip()) if row[5].strip() else None

                    # Handle date
                    try:
                        entry_date = datetime.strptime(row[6].strip(), "%Y-%m-%d").date()
                    except (ValueError, AttributeError):
                        print(f"Skipping row (invalid date): {row}")
                        error_count += 1
                        continue

                    # Validate foreign keys
                    cursor.execute("SELECT FoodID FROM Foods WHERE FoodID = %s", (food_id,))
                    if not cursor.fetchone():
                        print(f"Skipping row (invalid FoodID {food_id}): {row}")
                        error_count += 1
                        continue

                    cursor.execute("SELECT NutrientID FROM Nutrients WHERE NutrientID = %s", (nutrient_id,))
                    if not cursor.fetchone():
                        print(f"Skipping row (invalid NutrientID {nutrient_id}): {row}")
                        error_count += 1
                        continue

                    cursor.execute("SELECT NutrientSourceID FROM NutrientSources WHERE NutrientSourceID = %s", (nutrient_source_id,))
                    if not cursor.fetchone():
                        print(f"Skipping row (invalid NutrientSourceID {nutrient_source_id}): {row}")
                        error_count += 1
                        continue

                    # Insert into NutrientAmounts
                    sql = """
                    INSERT INTO NutrientAmounts 
                    (FoodID, NutrientID, NutrientValue, StandardError, NumberOfObservations, NutrientSourceID, NutrientDateOfEntry)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        food_id,
                        nutrient_id,
                        nutrient_value,
                        standard_error,
                        num_observation,
                        nutrient_source_id,
                        entry_date
                    )
                    cursor.execute(sql, values)
                    success_count += 1

                except Exception as e:
                    print(f"Error in row: {e}")
                    error_count += 1
                    continue

            db_config.commit()
            print(f"Inserted {success_count} rows. Errors: {error_count}")

    except Exception as e:
        print(f"Fatal error: {e}")
        db_config.rollback()

insert_nutrients_amount()