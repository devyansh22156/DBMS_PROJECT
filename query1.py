import mysql.connector

def order_items():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dev123",
            database="kads"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        for product in products:
            print(product)  # Print each row of the product table

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    order_items()
