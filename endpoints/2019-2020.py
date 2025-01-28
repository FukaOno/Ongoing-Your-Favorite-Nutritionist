from flask import Flask, jsonify, request
import mysql.connector 
from mysql.connector import Error

app = Flask(__name__)

db_config= {
    "host": "3306",
    "user": "root", 
    "password": "fuka1010",
    "database": "mealplan"
}
