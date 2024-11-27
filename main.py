from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import MySQLdb.cursors

load_dotenv()
app = Flask(__name__)
 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD')
app.config['MYSQL_DB'] = 'business_supply'
 
mysql = MySQL(app)

@app.route('/')
@app.route('/homescreen', methods=['GET', 'POST'])
def homescreen():
    employees = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM employees')
    employees = cursor.fetchone()
    return render_template('homescreen.html', employees=employees)

if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))