import mysql.connector

def order_items():
    try:
        connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dev123",
            database="kads"
        )
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        for product in products:
            print(product)

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if 'conn' in locals() and connect.is_connected():
            cursor.close()
            connect.close()


if __name__ == "__main__":
    order_items()
