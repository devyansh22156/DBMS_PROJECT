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

def fetch_user_data(user_id):
    connect = mysql.connector.connect(**db_config)
    cursor = connect.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer WHERE CustomerID = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connect.close()
    return user

@app.route('/customerHome.html')
def customerHome():
    return render_template('customerHome.html')

@app.route('/customer_profile.html')
def customer_profile():
    # Retrieve the user_id from the URL
    user_id_str = request.args.get('user_id')
    # Parse the user_id string into a dictionary
    user_id = ast.literal_eval(user_id_str)
    # Render the template with the user_id dictionary
    return render_template('customer_profile.html', user=user_id)
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            return "Email and password are required."
        connect = mysql.connector.connect(**db_config)
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer WHERE Email = %s AND Password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connect.close()
        if user:
            # Need to insert Main Home page Here
            # return render_template('/customer_profile.html', user=user)
            return render_template('/customerHome.html', user=user)
        else:
            return "Invalid email or password"
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
