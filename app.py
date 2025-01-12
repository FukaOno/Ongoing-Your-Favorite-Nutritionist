from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route('/api/nutrients', methods=['GET'])
def get_nutrients():
    # Open the CSV file
    with open("2021-2023 NutritionData(FNDDS).csv", "r") as mycsv:
        reader = csv.DictReader(mycsv)

        print(reader.fieldnames)
        
#         nutrients_needed=["Protein", "Total Fat", "Carbohydrate", "Energy"]

#         nutrients_data = {}

#         for line in reader:
#             ingredient = line["Ingredient description"]
#             nutrient = line["Nutrient description"]
#             value = line["Nutrient value"]

#             if nutrient in nutrients_needed:
#                 if ingredient not in nutrients_data:
#                     nutrients_data[ingredient] ={}

#                 nutrients_data[ingredient][nutrient]=float(value) if value else 0.0
#         # Return the data as JSON
#         return jsonify(data)

# if __name__ == '__main__':
#     app.run(debug=True)
