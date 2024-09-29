import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change if using a remote server
            database='student_db',  # Your database name
            user='root',  # MySQL username
            password='Agniswar@82!'  # MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
def register_student(connection, first_name, last_name, email, phone, course, registration_date):
    try:
        cursor = connection.cursor()  # Use the connection's cursor method
        query = """
            INSERT INTO students (first_name, last_name, email, phone, course, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (first_name,last_name, email, phone, course, registration_date)
        cursor.execute(query, data)
        connection.commit()  # Don't forget to commit the transaction!
        print(f"Student {first_name} registered successfully.")
    except mysql.connector.Error as error:
        print(f"Failed to register student: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")


if __name__=="__main__":
    connection = create_connection()
    if connection :
        register_student(connection,'Rajarshi', 'Roy','rajaeshi@gmail.com','0987654321','Information Technology','2024-09-28 ')
        connection.close()
