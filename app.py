from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dev123',
    'database': 'kads'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup.html', methods=['POST'])
def signup():
    if request.method == 'POST':
        customerid = request.form['customerid']
        fullname = request.form['fullname']
        email = request.form['email']
        contact = int(request.form['contact'])
        address1 = request.form['address1']
        address2 = request.form['address2']
        address3 = request.form['address3']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer (CustomerID, FullName, Email, ContactDetails, AddressLine1, AddressLine2, AddressLine3, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (customerid, fullname, email, contact, address1, address2, address3, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

@app.route('/login.html', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['login_email']
        password = request.form['login_password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE Email = %s AND Password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return f"Welcome, {user['FullName']}!"
        else:
            return "Invalid email or password"

if __name__ == '__main__':
    app.run(debug=True)
