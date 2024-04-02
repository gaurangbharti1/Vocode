from flask import Flask, redirect, render_template, request, jsonify, session, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='../frontend/', static_url_path='', static_folder='../frontend')

app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql3694990'
app.config['MYSQL_PASSWORD'] = 'bV4Nqi1Hiw'
app.config['MYSQL_DB'] = 'sql3694990'
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

        # Create the TeacherCourses table
    cur.execute('''CREATE TABLE IF NOT EXISTS TeacherCourses (
        teacher_id INT,
        course_id INT,
        PRIMARY KEY (teacher_id, course_id),
        FOREIGN KEY (teacher_id) REFERENCES Users(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
    )''')

    # Insert dummy users
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('John', 'Doe', '1990-01-01', 'john.doe@example.com', 'hashed_password', 'admin')")
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jane', 'Smith', '1992-02-02', 'jane.smith@example.com', 'hashed_password', 'teacher')")
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jim', 'Bean', '1994-03-03', 'jim.bean@example.com', 'hashed_password', 'student')")
    # insert dummy courses
    cur.execute("INSERT IGNORE INTO Courses (title, description, admin_id) VALUES ('Basic Programming', 'Learn the fundamentals of programming.', 1)")
    cur.execute("INSERT IGNORE INTO Courses (title, description, admin_id) VALUES ('Database Concepts', 'An introduction to relational databases.', 2)")
    cur.execute("INSERT IGNORE INTO Courses (title, description, admin_id) VALUES ('Web Development', 'Design and develop interactive websites.', 1)")
    cur.execute("INSERT IGNORE INTO Enrollment (student_id, course_id) VALUES (3, 1)")
    cur.execute("INSERT IGNORE INTO Enrollment (student_id, course_id) VALUES (3, 2)")
    cur.execute("INSERT IGNORE INTO Enrollment (student_id, course_id) VALUES (3, 3)")
    # Insert dummy teacher-course associations
    cur.execute("INSERT IGNORE INTO TeacherCourses (teacher_id, course_id) VALUES (2, 1)")
    cur.execute("INSERT IGNORE INTO TeacherCourses (teacher_id, course_id) VALUES (2, 2)")


    # Commit changes and close the connection
    print('Database initialized')
    print('Users:', cur.execute('SELECT * FROM Users'))

    mysql.connection.commit()
    cur.close()

@app.before_request
def initialize_assignments():
    cur = mysql.connection.cursor()

    # Clear the Assignments table
    cur.execute("DELETE FROM Assignments")

    # Check if the Assignments table is empty
    cur.execute("SELECT COUNT(*) as count FROM Assignments")
    result = cur.fetchone()
    if result['count'] == 0:
        # The table is empty, safe to insert dummy data
        cur.execute("INSERT INTO Assignments (title, type, content, course_id) VALUES ('Introduction to Programming', 'Homework', 'Complete the Python exercise.', 1)")
        cur.execute("INSERT INTO Assignments (title, type, content, course_id) VALUES ('Database Basics', 'Quiz', 'Take the SQL basics quiz.', 2)")
        print("Assignments inserted.")
    else:
        print("Assignments table was not empty after clearing.")

    mysql.connection.commit()
    cur.close()

@app.route('/')
def index():
    return render_template("webpages/login.html")

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()

    return render_template('webpages/profile.html', user=user_details)

@app.route('/assignments')
def assignments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT Assignments.id, Assignments.title, Assignments.type, Assignments.content, Courses.title AS course_title
                   FROM Assignments
                   JOIN Courses ON Assignments.course_id = Courses.id
                   JOIN Enrollment ON Courses.id = Enrollment.course_id
                   WHERE Enrollment.student_id = %s''', (user_id,))
    assignments = cur.fetchall()
    cur.close()

    return render_template('webpages/assignments.html', assignments=assignments)

@app.route('/teacher-classes')
def teacher_classes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT Courses.id, Courses.title, Courses.description
                   FROM TeacherCourses
                   JOIN Courses ON TeacherCourses.course_id = Courses.id
                   WHERE TeacherCourses.teacher_id = %s''', (user_id,))
    classes = cur.fetchall()
    cur.close()

    return render_template('webpages/teacher-classes.html', classes=classes)

@app.route('/student-classes')
def student_classes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT Courses.id, Courses.title, Courses.description
                   FROM Enrollment
                   JOIN Courses ON Enrollment.course_id = Courses.id
                   WHERE Enrollment.student_id = %s''', (user_id,))
    classes = cur.fetchall()
    cur.close()

    return render_template('webpages/student-classes.html', classes=classes)

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    birthdate = request.form['birthdate']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    role = request.form['role']
    print("role", role)
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400
    else:
        cur.execute("INSERT INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, birthdate, email, password, role))
        mysql.connection.commit()
    cur.close()
    return render_template("webpages/login.html")
    
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
        session['role'] = user_data['role']
        if user_data['role'] == 'admin':
            return render_template("webpages/admin-dashboard.html"), 200
        elif user_data['role'] == 'teacher':
            return render_template("webpages/teacher-dashboard.html"), 200
        else:
            return redirect(url_for('student_dashboard')), 200

    return "unsuccessful"

@app.route('/student-dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return "Unauthorized", 401

    user_id = session['user_id']
    
    cur = mysql.connection.cursor()

    cur.execute('''SELECT Courses.id, Courses.title, Courses.description, COUNT(Assignments.id) as assignment_count
                   FROM Enrollment
                   JOIN Courses ON Enrollment.course_id = Courses.id
                   LEFT JOIN Assignments ON Courses.id = Assignments.course_id
                   WHERE Enrollment.student_id = %s
                   GROUP BY Courses.id''', (user_id,))
    courses = cur.fetchall()
    cur.close()

    return render_template('webpages/student-dashboard.html', courses=courses)

<<<<<<< HEAD
@app.route('/teacher-dashboard')
def teacher_dashboard():
    if 'user_id' not in session or session['role'] != 'teacher':
        return "Unauthorized", 401

    teacher_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT Courses.id, Courses.title, Courses.description
                   FROM TeacherCourses
                   JOIN Courses ON TeacherCourses.course_id = Courses.id
                   WHERE TeacherCourses.teacher_id = %s''', (teacher_id,))
    courses = cur.fetchall()
    cur.close()

    return render_template('webpages/teacher-dashboard.html', courses=courses)


=======
>>>>>>> 20d9abebc5b1b06ecb8964d89de8d82ab2317f21
if __name__ == '__main__':
    app.run(debug=True)