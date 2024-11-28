from flask import Flask,render_template, request, session
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
    # employees = ''
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute(
    #     'SELECT * FROM employees')
    # employees = cursor.fetchone()
    return render_template('homescreen.html')

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    employee = ''
    if request.method == "POST" and 'username' in request.form:
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
        'SELECT username, taxid FROM employees where username = % s', (username, ))
        employee = cursor.fetchone()
    return render_template('employee.html', employee=employee)

@app.route('/owner', methods=['GET', 'POST'])
def owner():
    return render_template('owner.html')

@app.route('/driver', methods=['GET', 'POST'])
def driver():
    return render_template('driver.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    return render_template('product.html')

@app.route('/service', methods=['GET', 'POST'])
def service():
    return render_template('service.html')


@app.route('/van', methods=['GET', 'POST'])
def van():
    return render_template('van.html')

@app.route('/business_and_location', methods=['GET', 'POST'])
def business_and_location():
    return render_template('business_and_location.html')

@app.route('/views', methods=['GET', 'POST'])
def views():
    return render_template('views.html')

if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))