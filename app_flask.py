from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Function to establish the MySQL database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host = 'localhost', 
            database = 'student_db',  
            user= 'root',  
            password = 'Agniswar@82!'  
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


import re # For regular expression-based validatation
#Add functions to validate email, phone number, and password

def is_valid_email(email):
    #Regular expresiion for validation email format 
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(regex, email) is not None

def is_valid_phone(phone):
    #Ensuring the phone number contain only digits:
    return phone.isdigit() and len(phone) == 10

def is_valid_password(password):
    #check if the password has at least 8 char
    return len(password) >= 8


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

        #backend validation before inserting into the database
        if not is_valid_email(email):
            return "Invalid Email Format!!",400   #return a 400 Bad request error
        
        if not is_valid_phone(phone):
            return "Invalid Phone Number!!",400
        
        if not is_valid_password(password):
            return "Invalid Password!!",400
        
        #if the validation pass insert the data into the database

        connection = create_connection()
        if connection:
            register_student(connection, first_name, last_name, email, phone, course, registration_date, password)
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        #check for empty fields
        if not email or not password:
            return "Please Fill out all the Fields!"

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