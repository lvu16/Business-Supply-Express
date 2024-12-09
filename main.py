from flask import Flask, flash, redirect,render_template, request, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import MySQLdb.cursors
import logging
from helper_functions import *
#logging.basicConfig(filename="logs.log", filemode='w', level=logging.INFO)

load_dotenv()

app = Flask(__name__)

app.secret_key = 'C$suck$!'  # Replace 'your_secret_key' with something unique and secure.


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD')
app.config['MYSQL_DB'] = 'business_supply'
app.config['MYSQL_PORT'] = 3306
app.debug = True
 
mysql = MySQL(app)

#routing to main pages
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


@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if request.method == 'POST':
        username = request.form['username']
        licenseID = request.form['licenseID']
        license_type = request.form['license_type']
        driver_experience = request.form.get('driver_experience')

        # Input validation
        if not username or not licenseID or not license_type or not driver_experience:
            flash('All fields are required!', 'danger')
            return render_template('add_driver.html')

        try:
            driver_experience = int(driver_experience)  # Convert to integer
        except ValueError:
            flash('Driver experience must be a number!', 'danger')
            return render_template('add_driver.html')

        # Connect to MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        try:
            # Call the stored procedure
            cursor.callproc('add_driver_role', [username, licenseID, license_type, driver_experience])
            mysql.connection.commit()
            flash('Driver role added successfully!', 'success')
        except MySQLdb.Error as err:
            flash(f'Error: {err}', 'danger')
            app.logger.error(f'Error adding driver: {err}')
        finally:
            cursor.close()

        return redirect('/driver')  # Redirect to the driver home page

    # Render the form for GET requests
    return render_template('add_driver.html')


@app.route('/takeover_van', methods=['GET', 'POST'])
def takeover_van():
    if request.method == 'POST':
        username = request.form['username']
        van_id = request.form['van_id']
        tag = request.form['tag']

        # Input validation
        if not username or not van_id or not tag:
            flash('All fields are required!', 'danger')
            return render_template('takeover_van.html')

        try:
            tag = int(tag)  # Convert to integer
        except ValueError:
            flash('Tag must be a valid number!', 'danger')
            return render_template('takeover_van.html')

        # Connect to MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        try:
            # Call the stored procedure
            cursor.callproc('takeover_van', [username, van_id, tag])
            mysql.connection.commit()
            flash('Van successfully taken over!', 'success')
        except MySQLdb.Error as err:
            flash(f'Error: {err}', 'danger')
            app.logger.error(f'Error taking over van: {err}')
        finally:
            cursor.close()

        return redirect('/driver')  # Redirect to the driver home page

    # Render the form for GET requests
    return render_template('takeover_van.html')


@app.route('/remove_driver', methods=['GET', 'POST'])
def remove_driver():
    if request.method == 'POST':
        username = request.form['username']

        # Input validation
        if not username:
            flash('Username is required!', 'danger')
            return render_template('remove_driver.html')

        # Connect to MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        try:
            # Call the stored procedure
            cursor.callproc('remove_driver_role', [username])
            mysql.connection.commit()
            flash('Driver successfully removed!', 'success')
        except MySQLdb.Error as err:
            flash(f'Error: {err}', 'danger')
            app.logger.error(f'Error removing driver: {err}')
        finally:
            cursor.close()

        return redirect('/driver')  # Redirect to the driver home page

    # Render the form for GET requests
    return render_template('remove_driver.html')




@app.route('/product', methods=['GET', 'POST'])
def product():
    return render_template('product.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Fetch form data
        barcode = request.form['barcode']
        name = request.form['name']
        weight = request.form['weight']

        # Input validation
        if not barcode or not name or not weight:
            flash('All fields are required!', 'danger')
            return render_template('add_product.html')

        try:
            # Validate weight as an integer
            weight = int(weight)

            # Connect to MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Call the stored procedure
            cursor.callproc('add_product', [barcode, name, weight])
            mysql.connection.commit()

            flash('Product added successfully!', 'success')
        except ValueError:
            flash('Weight must be a valid number!', 'danger')
        except Exception as err:
            flash(f'Error: {str(err)}', 'danger')
            app.logger.error(f'Error adding product: {err}')
        finally:
            cursor.close()
        
        return redirect('/product')  # Redirect to the product page after adding

    # Render the form for GET requests
    return render_template('add_product.html')



@app.route('/purchase_product', methods=['GET', 'POST'])
def purchase_product():
    if request.method == 'POST':
        # Fetch form data
        long_name = request.form['long_name']
        van_id = request.form['id']
        tag = request.form['tag']
        barcode = request.form['barcode']
        quantity = request.form['quantity']

        # Input validation
        if not all([long_name, van_id, tag, barcode, quantity]):
            flash('All fields are required!', 'danger')
            return render_template('purchase_product.html')
        
        try:
            # Ensure quantity is a valid integer
            quantity = int(quantity)

            # Use MySQL connection pool and DictCursor
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Call the stored procedure
            cursor.callproc('purchase_product', [long_name, van_id, tag, barcode, quantity])
            mysql.connection.commit()

            flash('Product purchased successfully!', 'success')
        except ValueError:
            flash('Quantity must be a valid number!', 'danger')
        except MySQLdb.Error as err:
            flash(f'Error: {err}', 'danger')
            app.logger.error(f'Error during purchase_product: {err}')
        finally:
            cursor.close()

        return redirect('/product')  # Redirect to the procedures page

    # Render the form for GET requests
    return render_template('purchase_product.html')


@app.route('/remove_product', methods=['GET', 'POST'])
def remove_product():
    if request.method == 'POST':
        # Fetch form data
        barcode = request.form['barcode']

        # Input validation
        if not barcode:
            flash('Barcode is required!', 'danger')
            return render_template('remove_product.html')

        # Use MySQL connection pool and DictCursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        try:
            # Call the stored procedure
            cursor.callproc('remove_product', [barcode])
            mysql.connection.commit()
            flash('Product removed successfully!', 'success')
        except MySQLdb.Error as err:
            # Log the error for debugging
            app.logger.error(f"Error in remove_product: {err}")
            flash('An error occurred while removing the product. Please try again.', 'danger')
        finally:
            cursor.close()

        return redirect('/product')  # Redirect to the procedures page

    # Render the form for GET requests
    return render_template('remove_product.html')


@app.route('/service', methods=['GET', 'POST'])
def service():
    return render_template('service/service.html')


@app.route('/van', methods=['GET', 'POST'])
def van():
    return render_template('van/van.html')

@app.route('/business_and_location', methods=['GET', 'POST'])
def business_and_location():
    return render_template('business_and_location/business_and_location.html')

@app.route('/views', methods=['GET', 'POST'])
def views():
    return render_template('views.html')



@app.route('/product_view', methods=['GET'])
def product_view():
    # Connect to MySQL and fetch the data
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cursor.execute("SELECT * FROM display_product_view")
        product_data = cursor.fetchall()  # Fetch all rows from the view
    except MySQLdb.Error as err:
        flash(f"Error: {err}", "danger")
        product_data = []
    finally:
        cursor.close()
    
    # Render the data in a template
    return render_template('product_view.html', product_data=product_data)


@app.route('/driver_views', methods=['GET'])
def view_drivers():
    try:
        # Use MySQL connection pool and DictCursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Execute query to fetch data from the view
        cursor.execute("SELECT * FROM display_driver_view")
        drivers = cursor.fetchall()  # Fetch all rows

    except MySQLdb.Error as err:
        flash(f"Error fetching driver view: {err}", 'danger')
        drivers = []  # Return an empty list in case of error
    finally:
        cursor.close()

    return render_template('driver_views.html', drivers=drivers)


# OWNER view
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


# EMPLOYEE view
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


# OWNER procedures start funding
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


# OWNER produre add owner
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
                cursor.callproc('add_owner', [username, fname, lname, address, 
                                                    bdate])
                conn.commit()
                cursor.execute(
                    'SELECT username FROM business_owners where username = % s', (username))
                msg = cursor.fetchone()
                cursor.close()
            except Exception as e:
                msg = "owner could not be added " + str(e)
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the owner could not be added."
    return render_template('owner/add_owner.html', msg=msg)

# EMPLOYEE procedure hire employee
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
                cursor.execute(
                'SELECT username, id FROM work_for where username = % s and id = % s', (username, id))
                employee = cursor.fetchone()

            except Exception as e:
                print("user could not be hired " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the employee could not be hired."
            else:
                msg = employee
    return render_template('employee/hire_employee.html', msg=msg)

# EMPLOYEE procedure fire employee
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

                cursor.execute(
                    'SELECT username, id FROM work_for where username = % s and id = % s', (username, id))
                employee = cursor.fetchone()
                cursor.close()
                if employee:
                    msg = f"Cannot fire employee {username} with id {id} due to constraints"
                else:
                    msg = f"Employee {username} with id {id} successfully removed"
            except Exception as e:
                print("user could not be fired " + str(e))
                conn.rollback()
            finally:
                cursor.close()
            if msg == None:
                msg = "Due to contraints, the employee could not be fired."
    return render_template('employee/fire_employee.html', msg=msg)

# EMPLOYEE procedure add employee    
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

# VAN procedure add van
@app.route('/add_van', methods=['GET', 'POST'])
def add_van():
    msg = ''
    values = ['vanID', 'vanTag', 'fuel', 'capacity', 'sale']
    if request.method == 'POST':
        msg = check_request_form(request.form, values)
        if msg == '':
            id = to_string(request.form['vanID'])
            tag = to_int(request.form['vanTag'])
            fuel = to_int(request.form['fuel'])
            capacity = to_int(request.form['capacity'])
            sale = to_int(request.form['sale'])
            drivenBy = to_string(request.form['drivenBy'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()

                cursor.execute(
                    'SELECT id, tag, fuel, capacity, sales, driven_by FROM vans where id = % s and tag = % s', (id, tag))
                van = cursor.fetchone()
                if van and van[2] == fuel and van[3] == capacity and van[4] == sale and van[5] == drivenBy:
                    return render_template('van/add_van.html', msg=f'Van {id} tag {tag} already exists')


                cursor.callproc('add_van', [id, tag, fuel, capacity, sale, drivenBy])
                conn.commit()
                cursor.execute(
                    'SELECT id, tag, fuel, capacity, sales, driven_by FROM vans where id = % s and tag = % s', (id, tag))
                van = cursor.fetchone()
                if van and van[2] == fuel and van[3] == capacity and van[4] == sale and van[5] == drivenBy:
                    msg = f'Van {id} tag {tag} successfully added'
                else:
                    msg = "Van could not be added due to constraints."
            except Exception as e:
                print("van could not be added " + str(e))
                msg = f"An error occurs while adding van: {e}"
            finally:
                cursor.close()

    return render_template('van/add_van.html', msg=msg)

# VAN procedure remove van
@app.route('/remove_van', methods=['GET', 'POST'])
def remove_van():
    msg = ''
    values = ['vanID', 'vanTag']
    if request.method == 'POST':
        msg = check_request_form(request.form, values)
        if msg == '':
            id = to_string(request.form['vanID'])
            tag = to_string(request.form['vanTag'])
        
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id, tag FROM vans where id = % s and tag = % s', (id, tag))
                van = cursor.fetchone()
                if van == None:
                    return render_template('van/remove_van.html', msg = f'Van {id} tag {tag} is not in the database')
                cursor.callproc('remove_van', [id, tag])
                conn.commit()
                cursor.execute(
                    'SELECT id, tag FROM vans where id = % s and tag = % s', (id, tag))
                van = cursor.fetchone()
                cursor.close()
                if van:
                    msg = f"Cannot remove van {id} tag {tag} due to constraints"
                else:
                    msg = f"Van {id} tag {tag} successfully removed"
            except Exception as e:
                print("van could not be removed: " + str(e))
                msg = f"An error occurs while removing van: {e}"
            finally:
                cursor.close()

    return render_template('van/remove_van.html', msg = msg)

# VAN procedure load van
@app.route('/load_van', methods=['GET', 'POST'])
def load_van():
    msg = ''
    values = ['vanID', 'vanTag', 'barcode', 'price']
    if request.method == 'POST':
        msg = check_request_form(request.form, values)
        if msg == '':
            id = to_string(request.form['vanID'])
            tag = to_int(request.form['vanTag'])
            barcode = to_string(request.form['barcode'])
            morePackages = to_int(request.form['morePackages'])
            price = to_int(request.form['price'])
            
            try:
                conn = mysql.connection
                cursor = conn.cursor()

                cursor.execute(
                    'SELECT id, tag, barcode, quantity, price FROM contain where id = %s and tag = %s and barcode = %s', (id, tag, barcode))
                product = cursor.fetchone()

                if product and product[4] != price:
                    return render_template('van/load_van.html', msg= f'product with barcode {barcode} already exists on van {id} tag {tag} with price {product[4]}')

                if product:
                    old_quantity = product[3]
                    expected_quantity = old_quantity + morePackages
                else:
                    expected_quantity = morePackages

                cursor.callproc('load_van', [id, tag, barcode, morePackages, price])
                conn.commit()

                cursor.execute(
                    'SELECT id, tag, barcode, quantity, price FROM contain where id = %s and tag = %s and barcode = %s', (id, tag, barcode))
                product = cursor.fetchone()
                cursor.close()
    
                if product and product[3] == expected_quantity and product[4] == price:
                    msg = f'product with barcode {barcode} is loadded successfully on van {id} tag {tag}'
                else:
                    msg = "Cannot load product due to constrains"
            except Exception as e:
                print("van could not be added " + str(e))
                msg = f"An error occurs while loading van: {e}"
            finally:
                cursor.close()

    return render_template('van/load_van.html', msg=msg)

#VAN procedure drive van
@app.route('/drive_van', methods=['GET', 'POST'])
def drive_van():
    msg =''
    values = ['vanID', 'vanTag', 'destination']
    if request.method == 'POST':
        msg = check_request_form(request.form, values)
        if msg == '':
            id = to_string(request.form['vanID'])
            tag = to_int(request.form['vanTag'])
            destination = to_string(request.form['destination'])

            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id, tag, located_at FROM vans where id = %s and tag = %s and located_at = %s', (id, tag, destination))
                van = cursor.fetchone()
                if van: 
                     return render_template('van/drive_van.html', msg = f'Van {id} tag {tag} is already at location {destination}')
                cursor.callproc('drive_van', [id, tag, destination])
                conn.commit()
                cursor.execute(
                    'SELECT id, tag, located_at FROM vans where id = %s and tag = %s and located_at = %s', (id, tag, destination))
                van = cursor.fetchone()
                cursor.close()

                if van and van[2] == destination:
                    msg = f'Van {id} tag {tag} successfully moved to {destination}'
                else:
                    msg = "Van could not be moved due to constraints or the van might not have enough fuel."
            except Exception as e:
                print("cannot drive the van" + str(e))
                msg = f'An error occurred while driving the van: {e}'
                conn.rollback()
            finally:
                cursor.close()

    return render_template('van/drive_van.html', msg = msg)

# VAN procedure refuel van
@app.route('/refuel_van', methods=['GET', 'POST'])
def refuel_van():
    msg = ''
    values = ['vanID', 'vanTag', 'more_fuel']
    if request.method == 'POST':
        msg = check_request_form(request.form, values)
        if msg == '':
            id = to_string(request.form['vanID'])
            tag = to_int(request.form['vanTag'])
            more_fuel = to_int(request.form['more_fuel'])
            try:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id, tag, fuel FROM vans where id = %s and tag = %s', (id, tag))
                van = cursor.fetchone()
                if van:
                    old_fuel = van[2]
                else:
                    return render_template('van/refuel_van.html', msg = f'Van {id} tag {tag} does not exist')
               
                cursor.callproc('refuel_van', [id, tag, more_fuel])
                conn.commit()

                cursor.execute(
                    'SELECT id, tag, fuel FROM vans where id = %s and tag = %s', (id, tag))
                updated_van = cursor.fetchone()
                new_fuel = updated_van[2]
                expected_fuel = old_fuel + more_fuel
                cursor.close()
                
                if new_fuel == expected_fuel:
                    msg = f'Van {id} tag {tag} is refueled successfully'
                else:
                    msg = f"Van {id} tag {tag} could not be refueled due to constraints."
            except Exception as e:
                print("van could not be refueled " + str(e))
                msg = f"An error occurs while refueling van: {e}"
            finally:
                cursor.close()
    return render_template('van/refuel_van.html', msg = msg)

@app.route('/add_worker_role', methods=['GET', 'POST'])
def add_worker_role():
    msg = ""
    if request.method == "POST":
        username = request.form['username']
        try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.callproc('add_worker_role', [username])
            conn.commit()
            cursor.execute(
                'SELECT username FROM workers where username = %s', (username,))
            msg = cursor.fetchone()
            cursor.close()
        except Exception as e:
            msg = "Worker role could not be added: " + str(e)
            conn.rollback()
        finally:
            cursor.close()
        if msg is None:
            msg = "Due to constraints, the worker role could not be added"
    return render_template('employee/add_worker_role.html', msg=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

