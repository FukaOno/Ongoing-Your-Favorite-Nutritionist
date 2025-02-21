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