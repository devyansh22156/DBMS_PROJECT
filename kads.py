import mysql.connector
import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dev123',
    'database': 'kads'
}

class Customer:
    def __init__(self, customer_id, full_name, email, contact_details, address_line1,
                 address_line2=None, address_line3=None, password=None):
        self.customer_id = customer_id
        self.full_name = full_name
        self.email = email
        self.contact_details = contact_details
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.password = password

def fetch_customer_by_email_password(email, password):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = "SELECT CustomerID, FullName, Email, ContactDetails, AddressLine1, AddressLine2, AddressLine3, Password FROM customer WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password))
        customer_data = cursor.fetchone()
        if customer_data:
            return Customer(*customer_data)
        else:
            print("Invalid email or password!")
            return None
    except mysql.connector.Error as error:
        print("Failed to log in:", error)
        return None
    finally:
        if 'connection' in locals() or 'connection' in globals():
            connection.close()

def display_products():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = "SELECT ProductID, Name, Price FROM product"
        cursor.execute(query)
        products = cursor.fetchall()
        for product in products:
            print(product)
    except mysql.connector.Error as error:
        print("Failed to fetch products:", error)
    finally:
        if 'connection' in locals() or 'connection' in globals():
            connection.close()

def buy_gadgets(customer_id):
    while True:
        display_products()
        product_id = input("Enter product ID: ")
        quantity = int(input("Enter quantity: "))

        # Add product to cart and calculate cost
        add_to_cart(product_id, customer_id, quantity)

        choice = input("Press 'C' to continue shopping or 'X' to checkout: ")
        if choice.upper() == 'X':
            break

def add_to_cart(product_id, customer_id, quantity):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = "INSERT INTO cart (ProductID, Quantity, CustomerID) VALUES (%s, %s, %s)"
        cursor.execute(query, (product_id, quantity, customer_id))
        connection.commit()
        print("Product added to cart successfully!")
    except mysql.connector.Error as error:
        print("Failed to add product to cart:", error)
    finally:
        if 'connection' in locals() or 'connection' in globals():
            connection.close()

def main():
    while True:
        print("\n1. SignUp")
        print("2. LogIn")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            full_name = input("Enter full name: ")
            email = input("Enter email: ")
            contact_details = input("Enter contact details: ")
            address_line1 = input("Enter address line 1: ")
            address_line2 = input("Enter address line 2 (optional): ")
            address_line3 = input("Enter address line 3 (optional): ")
            password = input("Enter password: ")
            customer = Customer(full_name, email, contact_details, address_line1, address_line2, address_line3, password)
            customer.signup()
        elif choice == '2':
            email = input("Enter Email: ")
            password = input("Enter password: ")
            logged_in_customer = fetch_customer_by_email_password(email, password)
            if logged_in_customer:
                print("Logged in successfully!")
                while True:
                    print("\n1. Buy Gadgets")
                    print("2. Display Profile")
                    print("3. Logout")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        buy_gadgets(logged_in_customer.customer_id)
                    elif choice == '2':
                        print(logged_in_customer.__dict__)  # Print customer object attributes
                    elif choice == '3':
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
