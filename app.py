from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/nutrients', methods=['GET'])
def get_nutrients():

    #Specific nutrients value that I am looking for
    nutrients_needed = ["Protein", "Total Fat", "Carbohydrate", "Energy"]
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
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500

    return jsonify(nutrients_data)

if __name__ == '__main__':
    app.run(debug=True)