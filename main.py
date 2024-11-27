from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
 

app.config['MYSQL_HOST'] = os.getenv('LOCALHOST')
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD')
app.config['MYSQL_DB'] = 'business_supply'
 
mysql = MySQL(app)