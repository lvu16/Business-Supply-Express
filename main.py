from flask import Flask, flash, redirect,render_template, request, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import MySQLdb.cursors

load_dotenv()

app = Flask(__name__)

app.secret_key = 'C$suck$!'  # Replace 'your_secret_key' with something unique and secure.


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv('MYSQLPASSWORD'))
