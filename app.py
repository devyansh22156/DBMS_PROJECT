import mysql.connector
import datetime
import ast

class Customer:
    def __init__(self, fullname, email, contact, address1, address2, address3, password, security_question, security_answer):
        self.fullname = fullname
        self.email = email
        self.contact = contact
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer

    def save_to_database(self, db_manager):
        db_manager.insert_customer(self)

    @staticmethod
    def from_dict(data):
        return Customer(**data)

class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        return mysql.connector.connect(**self.db_config)

    def insert_customer(self, customer):
        connect = self.connect()
        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO customer (FullName, Email, ContactDetails, AddressLine1, AddressLine2, AddressLine3, Password, SecurityQuestion, SecurityAnswer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (customer.fullname, customer.email, customer.contact, customer.address1, customer.address2, customer.address3, customer.password, customer.security_question, customer.security_answer))
        connect.commit()
        cursor.close()
        connect.close()

# Define other classes (Product, Cart) similarly

def main():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'dev123',
        'database': 'kads'
    }



if __name__ == "__main__":
    main()
