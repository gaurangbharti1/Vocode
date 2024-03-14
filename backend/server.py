from flask import Flask, render_template, request, jsonify, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder='../frontend', static_url_path='', static_folder='../frontend')

app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql3691381'
app.config['MYSQL_PASSWORD'] = 'MN4ufRH1tb'
app.config['MYSQL_DB'] = 'sql3691381'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'test_key'

bcrypt = Bcrypt(app)
mysql = MySQL(app)

@app.before_request
def initialize_database():
    cur = mysql.connection.cursor()
    
    # Create the Users table
    cur.execute('''CREATE TABLE IF NOT EXISTS Users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        date_of_birth DATE,
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        role ENUM('admin', 'teacher', 'student')
    )''')

    # Create the Courses table
    cur.execute('''CREATE TABLE IF NOT EXISTS Courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        admin_id INT,
        FOREIGN KEY (admin_id) REFERENCES Users(id)
    )''')

    # Create the Assignments table
    cur.execute('''CREATE TABLE IF NOT EXISTS Assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        type VARCHAR(255),
        content TEXT,
        course_id INT,
        FOREIGN KEY (course_id) REFERENCES Courses(id)
    )''')

    # Create the Enrollment table
    cur.execute('''CREATE TABLE IF NOT EXISTS Enrollment (
        student_id INT,
        course_id INT,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES Users(id),
        FOREIGN KEY (course_id) REFERENCES Courses(id)
    )''')

    # Create the Grades table
    cur.execute('''CREATE TABLE IF NOT EXISTS Grades (
        student_id INT,
        assignment_id INT,
        grade INT,
        PRIMARY KEY (student_id, assignment_id),
        FOREIGN KEY (student_id) REFERENCES Users(id),
        FOREIGN KEY (assignment_id) REFERENCES Assignments(id)
    )''')

    # Insert dummy users
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('John', 'Doe', '1990-01-01', 'john.doe@example.com', 'hashed_password', 'admin')")
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jane', 'Smith', '1992-02-02', 'jane.smith@example.com', 'hashed_password', 'teacher')")
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jim', 'Bean', '1994-03-03', 'jim.bean@example.com', 'hashed_password', 'student')")

    # Commit changes and close the connection
    print('Database initialized')
    print('Users:', cur.execute('SELECT * FROM Users'))

    mysql.connection.commit()
    cur.close()

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    birthdate = request.form['birthdate']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400
    else:
        cur.execute("INSERT INTO Users (first_name, last_name, date_of_birth, email, password) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, birthdate, email, password))
        mysql.connection.commit()
    cur.close()
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    raw_password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE email = %s", (username,))
    user_data = cur.fetchone()
    cur.close()

    if user_data and user_data['password'] == raw_password:
        session['user_id'] = user_data['id']
        return "successful"

    return "unsuccessful"

if __name__ == '__main__':
    app.run(debug=True)