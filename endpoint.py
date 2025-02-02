from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    "host": "3306",
    "user": "root",
    "password": "fuka1010"
    "database": "mealplan"

}

def db_init():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients(
                id INT AUTO_INCREMENT PRIMARY KEY,
                ingredient_name VARCHAR(255) UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nutrient_values(
                id INT AUTO_INCREMENT PRIMARY KEY,
                ingredient_id INT,
                protein FLOAT,
                fat FLOAT,
                carbs FLOAT,
                calories INT,
                FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
            )
        """)

        connection.commit()
        print("Database initialized successfully")

        except Error as e:
            print(f"Error Initializing DataBase: {e}")
        finally:
            if "connection" in locals() and connection_is_connected():
                cursor.close()
                connection.close()


@app.route('/api/nutrients/db', methods=['GET'])
def get_nutrients():

    #Specific nutrients value that I am looking for
    nutrients_needed = ["Protein", "Total Fat", "Carbohydrate", "Energy", "Vitamin C", "Vitamin D", "Vitamin E"]
    nutrients_data = {}

    try:
       
        with open("2021-2023 NutritionData(FNDDS).csv", "r", newline='') as mycsv:
            
            #Process header
            headers = mycsv.readline().strip().strip('"').split(',') #first line -> list
            # print("Processed headers:", headers)
            
            #get the indicies of necessary cols
            ingredient_col = headers.index("Ingredient description")
            nutrient_col = headers.index("Nutrient description")
            value_col = headers.index("Nutrient value")
            
            #Process each line
            for line in mycsv:
                
                row = line.strip().strip('"').split('","')
                if len(row) == 1: #if the line is single string
                    row = row[0].split(',')
                
                #remove all the quotes
                row = [field.strip('"') for field in row]
                
                if len(row) <= max(ingredient_col, nutrient_col, value_col):
                    print(f"Skipping invalid row: {row}")
                    continue
                
                ingredient = row[ingredient_col]  #By using the index gotten from the necessary cols
                nutrient = row[nutrient_col]
                value = row[value_col]
                
                if nutrient in nutrients_needed:
                    if ingredient not in nutrients_data:
                        nutrients_data[ingredient] = {}
                    try:
                        nutrients_data[ingredient][nutrient] = float(value) if value else 0.0
                    except ValueError:
                        print(f"Could not convert value to float: {value}")
                        nutrients_data[ingredient][nutrient] = 0.0
    
        store_nutrients_data(nutrients_data)

        return jsonify(nutrients_data)
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500

def store_nutrients_data(nutrients_data):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        for ingredient, nutrients in nutrients_data.items():
            cursor.execute("""
                INSERT IGNORE INTO ingredients(ingredient_name)
                VALUES (%s)
        """, (ingredient,))

        cursor.execute("""
            SELECT id FROM ingredients WHERE ingredient_name = %s""", (ingredient,))
                ingredient_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO nutrient_values
            (ingredient_id, protein, total_fat, carbohydrate, energy)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            protein = VALUES(protein),
            fat = VALUES(total_fat),
            carbohydrate = VALUES(carbohydrate),
            energy = VALUES(energy)
        """, (
            ingredient_id,
            nutrients.get('Protein', 0.0),
            nutrients.get('Total Fat', 0.0),
            nutrients.get('Carbohydrate', 0.0),
            nutrients.get('Energy', 0.0)
            ))

        connection.commit()
        print("Data successfully stored in database")

        except Error as e:
            print(f"Error storing data: {e}")
            connection.rollback()
        finally:
            if "connection" in locals() and connection_is_connected():
                cursor.close()
                connection.close()

@app.route('/api/nutrients/db', methods=['GET'])
def get_nutrients_from_db():
    #continue from here

if __name__ == '__main__':
    app.run(debug=True)