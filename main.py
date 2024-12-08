from flask import Flask,render_template, request, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import MySQLdb.cursors
import logging
from helper_functions import *
#logging.basicConfig(filename="logs.log", filemode='w', level=logging.INFO)

load_dotenv()
app = Flask(__name__)
 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD')
app.config['MYSQL_DB'] = 'business_supply'
app.config['MYSQL_PORT'] = 3306
app.debug = True
 
mysql = MySQL(app)


@app.route('/')
@app.route('/homescreen', methods=['GET', 'POST'])
def homescreen():
    return render_template('homescreen.html')

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    return render_template('employee/employee.html')

@app.route('/owner', methods=['GET', 'POST'])
def owner():
    return render_template('owner/owner.html')

@app.route('/driver', methods=['GET', 'POST'])
def driver():
    return render_template('driver.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    return render_template('product.html')

@app.route('/service', methods=['GET', 'POST'])
def service():
    return render_template('service/service.html')


@app.route('/van', methods=['GET', 'POST'])
def van():
    return render_template('van.html')

@app.route('/business_and_location', methods=['GET', 'POST'])
def business_and_location():
    return render_template('business_and_location/business_and_location.html')

@app.route('/views', methods=['GET', 'POST'])
def views():
    return render_template('views.html')

@app.route('/owner_view', methods=['GET', 'POST'])
def owner_view():
    msg = ""
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * from display_owner_view')
        results = cursor.fetchall()
        cursor.close()
    except Exception as e:
        msg = "View could not be created: " + str(e)
        conn.rollback()
    finally:
        cursor.close()
    return render_template('owner/owner_view.html', msg=msg, results=results)

@app.route('/employee_view', methods=['GET', 'POST'])
def employee_view():
    msg = ""
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * from display_employee_view')
        results = cursor.fetchall()
        cursor.close()
    except Exception as e:
        msg = "View could not be created: " + str(e)
        conn.rollback()
    finally:
        cursor.close()
    return render_template('employee/employee_view.html', msg=msg, results=results)

@app.route('/start_funding', methods=['GET', 'POST'])
def start_funding():
    msg = ""
    values = ['owner', 'amount', 'longname', 'funddate']

    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            owner = to_string(request.form['owner'])
            amount = to_int(request.form['amount'])
            longname = to_string(request.form['longname'])
            funddate = get_date(request.form['funddate'])
            if type(funddate) == str:
                msg += funddate
                return render_template('owner/start_funding.html', msg=msg)
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('start_funding', [owner, amount, longname, funddate])
                conn.commit()
                cursor.execute(
                    'SELECT username, invested, business FROM fund where username = % s', (owner, ))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("owner investment could not be added " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the owner investment could not be added"
    return render_template('owner/start_funding.html', msg=msg)

@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    msg = ""
    values = ['username', 'fname', 'lname', 'address', 
              'bdate']

    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            username = to_string(request.form['username'])
            fname = to_string(request.form['fname'])
            lname = to_string(request.form['lname'])
            address = to_string(request.form['address'])
            bdate = get_date(request.form['bdate'])
            if type(bdate) == str:
                msg += bdate
                return render_template('owner/add_owner.html', msg=msg)
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('add_employee', [username, fname, lname, address, 
                                                    bdate])
                conn.commit()
                cursor.execute(
                    'SELECT username, fname FROM business_owners where username = % s and fname = % s', (username, fname))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("owner could not be added " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the owner could not be added."
    return render_template('owner/add_owner.html', msg=msg)


@app.route('/hire_employee', methods=['GET','POST'])
def hire_employee():
    msg = ""
    values = ['username', 'id']
    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            username = to_string(request.form['username'])
            id = to_string(request.form['id'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('hire_employee', [username, id])
                conn.commit()
                cursor.execute(
                    'SELECT username, id FROM work_for where username = % s and id = % s', (username, id))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("user could not be hired " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the employee could not be hired."
    return render_template('employee/hire_employee.html', msg=msg)

@app.route('/fire_employee', methods=['GET','POST'])
def fire_employee():
    msg = ""
    values = ['username', 'id']
    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            username = to_string(request.form['username'])
            id = to_string(request.form['id'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('fire_employee', [username, id])
                conn.commit()
                cursor.close()
            except Exception as e:
                print("user could not be fired " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the employee could not be fired."
    return render_template('employee/fire_employee.html', msg=msg)
    
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    msg = ""
    values = ['username', 'fname', 'lname', 'address', 
              'bdate', 'taxid', 'hiredate', 'experience', 'salary']

    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            username = to_string(request.form['username'])
            fname = to_string(request.form['fname'])
            lname = to_string(request.form['lname'])
            address = to_string(request.form['address'])
            bdate = get_date(request.form['bdate'])
            if type(bdate) == str:
                msg += bdate
                return render_template('employee/add_employee.html', msg=msg)
            taxid = to_string(request.form['taxid'])
            hiredate = get_date(request.form['hiredate'])
            if type(hiredate) == str:
                msg += hiredate
                return render_template('employee/add_employee.html', msg=msg)
            experience = to_int(request.form['experience'])
            salary = to_int(request.form['salary'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('add_employee', [username, fname, lname, address, 
                                                    bdate, taxid, hiredate, experience, salary])
                conn.commit()
                cursor.execute(
                    'SELECT username, taxid FROM employees where username = % s', (username, ))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("user could not be added " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the employee could not be added"
    return render_template('employee/add_employee.html', msg=msg)

@app.route('/testdb')
def testdb():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        cursor.close()
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection failed: {str(e)}'

@app.route('/connection_info')
def connection_info():
    try:
        cursor = mysql.connection.cursor()
        
        # Basic connection test
        cursor.execute('SELECT VERSION()')
        version = cursor.fetchone()
        
        # Get current user
        cursor.execute('SELECT USER()')
        user = cursor.fetchone()
        
        # Get current database
        cursor.execute('SELECT DATABASE()')
        db = cursor.fetchone()
        
        cursor.close()
        
        info = {
            'user': user[0] if user else 'Unknown',
            'database': db[0] if db else 'Unknown',
            'version': version[0] if version else 'Unknown',
            'mysql_config': {
                'host': app.config['MYSQL_HOST'],
                'user': app.config['MYSQL_USER'],
                'database': app.config['MYSQL_DB'],
                'port': app.config['MYSQL_PORT']
            }
        }
        
        return f'Connection Info: {info}'
    except Exception as e:
        return f'Error getting connection info: {str(e)}'

@app.route('/simple_test')
def simple_test():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        cursor.close()
        return f'Connection successful! Test query returned: {result}'
    except Exception as e:
        return f'Connection failed: {str(e)}'

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    msg = ""
    values = ['id', 'long_name', 'home_base']

    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            id = to_string(request.form['id'])
            long_name = to_string(request.form['long_name'])
            home_base = to_string(request.form['home_base'])
            manager = to_string(request.form['manager']) if request.form['manager'] else None
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                print(f"Attempting to add service with values: id={id}, long_name={long_name}, home_base={home_base}, manager={manager}") #testing
                cursor.callproc('add_service', [id, long_name, home_base, manager])
                conn.commit()
                cursor.execute(
                    'SELECT id FROM delivery_services where id = %s', (id,))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("service could not be added " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to constraints, the service could not be added"
    return render_template('service/add_service.html', msg=msg)

@app.route('/manage_service', methods=['GET', 'POST'])
def manage_service():
    msg = ""
    values = ['username', 'id']

    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            username = to_string(request.form['username'])
            id = to_string(request.form['id'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('manage_service', [username, id])
                conn.commit()
                cursor.execute(
                    'SELECT id FROM delivery_services where id = %s and manager = %s', (id, username))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("service manager could not be updated " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to constraints, the service manager could not be updated"
    return render_template('service/manage_service.html', msg=msg)

@app.route('/service_view', methods=['GET', 'POST'])
def service_view():
    msg = ""
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * from display_service_view')
        results = cursor.fetchall()
        cursor.close()
    except Exception as e:
        msg = "View could not be created: " + str(e)
        conn.rollback()
    finally:
        cursor.close()
    return render_template('service/service_view.html', msg=msg, results=results)

@app.route('/location_view', methods=['GET', 'POST'])
def location_view():
    msg = ""
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * from display_location_view')
        results = cursor.fetchall()
        cursor.close()
    except Exception as e:
        msg = "View could not be created: " + str(e)
        conn.rollback()
    finally:
        cursor.close()
    return render_template('business_and_location/location_view.html', msg=msg, results=results)

@app.route('/add_business', methods=['GET', 'POST'])
def add_business():
    msg = ""
    values = ['long_name', 'rating', 'spent', 'location']

    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            long_name = to_string(request.form['long_name'])
            rating = to_int(request.form['rating'])
            spent = to_int(request.form['spent'])
            location = to_string(request.form['location'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('add_business', [long_name, rating, spent, location])
                conn.commit()
                cursor.execute(
                    'SELECT long_name FROM businesses where long_name = %s', (long_name,))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("business could not be added " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to constraints, the business could not be added"
    return render_template('business_and_location/add_business.html', msg=msg)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    msg = ""
    values = ['label', 'x_coord', 'y_coord', 'space']

    if request.method == "POST":
        msg = check_request_form(request.form, values)
        if msg == '':
            label = to_string(request.form['label'])
            x_coord = to_int(request.form['x_coord'])
            y_coord = to_int(request.form['y_coord'])
            space = to_int(request.form['space'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.callproc('add_location', [label, x_coord, y_coord, space])
                conn.commit()
                cursor.execute(
                    'SELECT label FROM locations where label = %s', (label,))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print("location could not be added " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to constraints, the location could not be added"
    return render_template('business_and_location/add_location.html', msg=msg)

if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))