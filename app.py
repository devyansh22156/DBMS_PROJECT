from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime
import ast

userMain = None

app = Flask(__name__)

# Change these settings with your own machine specs
# Also don't forget to copy-paste and run dbQueryDump in default console before running the program

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dev123',
    'database': 'kads'
}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup.html', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        contact = request.form['contact']
        address1 = request.form['address1']
        address2 = request.form['address2']
        address3 = request.form['address3']
        password = request.form['password']
        customerid = str(datetime.date.today().year) + fullname.split()[0] + contact[5:10]
        contact = int(contact)

        connect = mysql.connector.connect(**db_config)
        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO customer (CustomerID, FullName, Email, ContactDetails, AddressLine1, AddressLine2, AddressLine3, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (customerid, fullname, email, contact, address1, address2, address3, password))
        connect.commit()
        cursor.close()
        connect.close()

        return redirect(url_for('index'))
    else:
        return render_template('/signup.html')

@app.route('/customerHome.html')
def customerHome():
    return render_template('customerHome.html')

@app.route('/getCustomerOrders.html')
def customerOders():
    # Not executed yet
    return render_template('/getCustomerOrder.html')

@app.route('/customer_profile.html')
def customer_profile():
    user_id_str = request.args.get('user_id')
    user_id = ast.literal_eval(user_id_str)
    return render_template('customer_profile.html', user=user_id)

@app.route('/get_products.html')
def getProductOnWeb():
    connect = mysql.connector.connect(**db_config)
    cursor = connect.cursor()
    cursor.execute(
        "SELECT * FROM PRODUCT"
    )
    inventory = cursor.fetchall()
    cursor.close()
    connect.close()
    return render_template('get_products.html', inventory=inventory)

# @app.route('/login.html', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         if not email or not password:
#             return "Email and password are required."
#         connect = mysql.connector.connect(**db_config)
#         cursor = connect.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM customer WHERE Email = %s AND Password = %s", (email, password))
#         user = cursor.fetchone()
#         cursor.close()
#         connect.close()
#         if user:
#             return render_template('/customerHome.html', user=user)
#         else:
#             return "Invalid email or password"
#     else:
#         return render_template('login.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            return "Email and password are required."
        connect = mysql.connector.connect(**db_config)
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT AccountLockedUntil FROM customer WHERE Email = %s", (email,))
        account_info = cursor.fetchone()
        if account_info and account_info['AccountLockedUntil']:
            remaining_lockout_time = account_info['AccountLockedUntil'] - datetime.datetime.now()
            if remaining_lockout_time.total_seconds() > 0:
                remaining_minutes = remaining_lockout_time.seconds // 60
                remaining_seconds = remaining_lockout_time.seconds % 60
                lockout_message = f"Your account is locked. Please try again in {remaining_minutes} minutes and {remaining_seconds} seconds."
                return render_template('/profileLock.html', lockout_message=lockout_message)
                # Need to add one html page here

        cursor.execute("SELECT * FROM customer WHERE Email = %s", (email,))
        user = cursor.fetchone()
        if user and user['Password'] == password:
            cursor.execute(
                "INSERT INTO LoginAttempts (CustomerID, Success) VALUES (%s, TRUE)",
                (user['CustomerID'],)
            )
            connect.commit()
            cursor.close()
            connect.close()
            return render_template('/customerHome.html', user=user)
        else:
            if user:
                cursor.execute(
                    "INSERT INTO LoginAttempts (CustomerID, Success) VALUES (%s, FALSE)",
                    (user['CustomerID'],)
                )
                connect.commit()
            cursor.close()
            connect.close()
            return render_template('/invalidEmailPass.html')
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
