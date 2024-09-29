from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Function to establish the MySQL database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            database = 'student_db',  # Your database name
            user= 'root',  # MySQL username
            password = 'Agniswar@82!'  # MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL Database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def register_student(connection, first_name, last_name, email, phone, course, registration_date, password):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO students (first_name, last_name, email, phone, course, registration_date, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (first_name, last_name, email, phone, course, registration_date, password)
        cursor.execute(query, data)
        connection.commit()
        print(f"Student {first_name} registered successfully.")
    except mysql.connector.Error as error:
        print(f"Failed to register student: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

@app.route('/')
def student_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        registration_date = request.form['registration_date']
        password = request.form['password']

        connection = create_connection()
        if connection:
            register_student(connection, first_name, last_name, email, phone, course, registration_date, password)
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM students WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            student = cursor.fetchone()
            cursor.close()
            connection.close()

            if student:
                return redirect(url_for('welcome'))
            else:
                return "Invalid Login Credential, Please Try Again!"
    return render_template('login.html')


@app.route('/welcome')
def welcome():
    return "<h1>Welcome. Registration Succesful</h1>"


if __name__ == "__main__":
    app.run(debug=True)