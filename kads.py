import mysql.connector
import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dev123',
    'database': 'kads'
}

class Customer:
    def __init__(self, full_name, email, contact_details, address_line1,
                 address_line2=None, address_line3=None, password=None,
                 order_history=None, membership_status=None,
                 account_locked_until=None, security_question=None,
                 security_answer=None):
        self.full_name = full_name
        self.email = email
        self.contact_details = contact_details
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.password = password
        self.order_history = order_history
        self.membership_status = membership_status
        self.account_locked_until = account_locked_until
        self.security_question = security_question
        self.security_answer = security_answer
        self.customer_id = self.generate_customer_id(contact_details)

    def generate_customer_id(self, contact_details):
        current_year = datetime.datetime.now().year
        last_5_digits = contact_details[-5:]
        return f"{current_year:04d}{self.full_name.replace(' ', '')}{last_5_digits}"

def fetch_customer_by_email_password(email, password):

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    query = "SELECT FullName, Email, ContactDetails, AddressLine1, AddressLine2, AddressLine3, Password FROM customer WHERE Email = %s AND Password = %s"
    cursor.execute(query, (email, password))
    customer_data = cursor.fetchone()
    print(customer_data)

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
            customer = Customer(full_name, email, contact_details,
                                address_line1, address_line2, address_line3, password)
            # customer.signup()  # Assuming signup method is implemented separately
        elif choice == '2':
            email = input("Enter Email: ")
            password = input("Enter password: ")
            customerID = fetch_customer_by_email_password(email, password)  # Corrected function call
            if customerID:
                print("Logged in successfully!")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
