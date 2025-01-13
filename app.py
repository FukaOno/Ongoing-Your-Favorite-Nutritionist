from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route('/api/nutrients', methods=['GET'])
def get_nutrients():
    # List of nutrients we want to track
    nutrients_needed = ["Protein", "Total Fat", "Carbohydrate", "Energy"]
    nutrients_data = {}

    try:
        # Open the CSV file
        with open("2021-2023 NutritionData(FNDDS).csv", "r", encoding='utf-8', newline='') as mycsv:
            # Read the first line and split it properly
            headers = mycsv.readline().strip().strip('"').split(',')
            print("Processed headers:", headers)
            
            # Find the correct column indices
            ingredient_col = headers.index("Ingredient description")
            nutrient_col = headers.index("Nutrient description")
            value_col = headers.index("Nutrient value")
            
            # Process each line manually
            for line in mycsv:
                # Clean and split the line
                row = line.strip().strip('"').split('","')
                if len(row) == 1:
                    row = row[0].split(',')
                
                print("Processing row:", row)  # Debug print
                
                # Remove any remaining quotes
                row = [field.strip('"') for field in row]
                
                if len(row) <= max(ingredient_col, nutrient_col, value_col):
                    print(f"Skipping invalid row: {row}")
                    continue
                
                ingredient = row[ingredient_col]
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
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500

    return jsonify(nutrients_data)

if __name__ == '__main__':
    app.run(debug=True)