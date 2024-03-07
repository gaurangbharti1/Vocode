from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql3689458'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sql3689458'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# Dummy data for users
users = [
    {'id': 1, 'username': 'user1', 'password': 'pass1'},
    {'id': 2, 'username': 'user2', 'password': 'pass2'},
    # Add more dummy users as needed
]

# Dummy data for other resources (e.g., posts)
posts = [
    {'id': 1, 'title': 'Post 1', 'content': 'Content of Post 1'},
    {'id': 2, 'title': 'Post 2', 'content': 'Content of Post 2'},
    # Add more dummy posts as needed
]

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
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Dummy registration logic (add user to the users list)
    new_user = {'id': len(users) + 1, 'username': username, 'password': password}
    users.append(new_user)

    return jsonify({'message': 'Registration successful', 'user': new_user})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Dummy login logic (check if user exists and password is correct)
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        return jsonify({'message': 'Login successful', 'user': user})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/posts', methods=['GET'])
def get_posts():
    # Dummy route to fetch posts
    return jsonify({'posts': posts})

if __name__ == '__main__':
    app.run(debug=True)