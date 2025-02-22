from flask import Flask, jsonify, request
import mysql.connector
import os
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    "host": os.getenv("DB_HOST", "3306"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "fuka1010"),
    "database": os.getenv("DB_NAME", "mealplan")

}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/generate-meal-plan', methods=['GET'])
def generate_meal_plan():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Missing user_id parameter'}), 400

        # Get user's historical data
        historical_meals = get_historical_meals(user_id)
        
        # Analyze nutritional balance
        nutrition_analysis = analyze_nutrition(historical_meals)
        
        # Generate personalized meal plan
        meal_plan = create_meal_plan(nutrition_analysis)
        
        return jsonify({
            'user_id': user_id,
            'meal_plan': meal_plan,
            'nutrition_summary': nutrition_analysis
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_historical_meals(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT meal_type, food_items, calories, protein, carbs, fats 
        FROM meals 
        WHERE user_id = %s AND date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

def analyze_nutrition(meals):
    total = {'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0}
    
    for meal in meals:
        total['calories'] += meal['calories']
        total['protein'] += meal['protein']
        total['carbs'] += meal['carbs']
        total['fats'] += meal['fats']
    
    # Calculate 7-day averages
    avg = {k: v/7 for k, v in total.items()}
    
    # Compare with recommended daily values
    recommendations = {
        'calories': 2000,
        'protein': 50,
        'carbs': 300,
        'fats': 70
    }
    
    analysis = {}
    for nutrient in total:
        analysis[nutrient] = {
            'average': avg[nutrient],
            'recommended': recommendations[nutrient],
            'difference': avg[nutrient] - recommendations[nutrient]
        }
    
    return analysis

def create_meal_plan(nutrition_analysis):
    # This is a simplified example - you'd want to implement actual meal logic
    # based on the nutritional differences and available food database
    
    meal_plan = {
        'breakfast': [],
        'lunch': [],
        'dinner': [],
        'snacks': []
    }
    
    # Example adjustment logic
    protein_diff = nutrition_analysis['protein']['difference']
    if protein_diff < -10:
        # Add protein-rich foods
        meal_plan['breakfast'].append('Greek yogurt with almonds')
        meal_plan['lunch'].append('Grilled chicken salad')
    
    # Add logic for other nutrients
    
    return meal_plan

if __name__ == '__main__':
    app.run(debug=True)