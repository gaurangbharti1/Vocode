
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='../frontend/', static_url_path='', static_folder='../frontend')

app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql3697454'
app.config['MYSQL_PASSWORD'] = 'NIHBljF31P'
app.config['MYSQL_DB'] = 'sql3697454'
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

    cur.execute('''CREATE TABLE IF NOT EXISTS Assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        type VARCHAR(255),
        content TEXT,
        course_id INT,
        FOREIGN KEY (course_id) REFERENCES Courses(id)
    )''')

    # Create the Assignments table
    cur.execute('''CREATE TABLE IF NOT EXISTS Assignment (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        description VARCHAR(255),
        dueDate DATE,
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

    if cur.execute('SELECT * FROM Users') == 0:
        # Insert dummy users
        cur.execute(f"INSERT INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('John', 'Doe', '1990-01-01', 'john.doe@example.com', 'hashed_password', 'admin')")
        cur.execute(f"INSERT INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jane', 'Smith', '1992-02-02', 'jane.smith@example.com', 'hashed_password', 'teacher')")
        cur.execute(f"INSERT INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jim', 'Bean', '1994-03-03', 'jim.bean@example.com', 'hashed_password', 'student')")

    if cur.execute('SELECT * FROM Courses') == 0:
        # insert dummy courses
        cur.execute("INSERT INTO Courses (title, description, admin_id) VALUES ('Basic Programming', 'Learn the fundamentals of programming.', 1)")
        cur.execute("INSERT INTO Courses (title, description, admin_id) VALUES ('Database Concepts', 'An introduction to relational databases.', 2)")
        cur.execute("INSERT INTO Courses (title, description, admin_id) VALUES ('Web Development', 'Design and develop interactive websites.', 1)")
        cur.execute("INSERT INTO Enrollment (student_id, course_id) VALUES (3, 1)")
        cur.execute("INSERT INTO Enrollment (student_id, course_id) VALUES (3, 2)")
        cur.execute("INSERT INTO Enrollment (student_id, course_id) VALUES (3, 3)")

    if cur.execute('SELECT * FROM TeacherCourses') == 0:
        # Insert dummy teacher-course associations
        cur.execute("INSERT INTO TeacherCourses (teacher_id, course_id) VALUES (2, 1)")
        cur.execute("INSERT INTO TeacherCourses (teacher_id, course_id) VALUES (2, 2)")
    
    # Commit changes and close the connection
    print('Database initialized')
    print('Users:', cur.execute('SELECT * FROM Users'))

    mysql.connection.commit()
    cur.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('webpages/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('webpages/500.html'), 500

@app.before_request
def initialize_assignments():
    cur = mysql.connection.cursor()

    # Check if the Assignments table is empty
    cur.execute("SELECT COUNT(*) as count FROM Assignment")
    result = cur.fetchone()
    if result['count'] == 0:
        # The table is empty, safe to insert dummy data
        cur.execute("INSERT INTO Assignment (title, description, dueDate, course_id) VALUES ('Introduction to Web Development', 'Complete the HTML and CSS exercise.', '2024-05-01', 1)")
        cur.execute("INSERT INTO Assignment (title, description, dueDate, course_id) VALUES ('Advanced Database Management', 'Read chapter 4 of the database textbook and answer questions 1-10.', '2024-06-15', 2)")
        print("Assignments inserted.")
    else:
        print("Assignments table was not empty")

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
    role = session['role']
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()

    if role == 'teacher':
        return render_template('webpages/profile-teacher.html', user=user_details)
    elif role == 'student':
        return render_template('webpages/profile.html', user=user_details)
    
@app.route('/assignments')
def assignments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT Assignment.id, Assignment.title, Assignment.description, Courses.title AS course_title
                   FROM Assignment
                   JOIN Courses ON Assignment.course_id = Courses.id
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

    return render_template('webpages/student-course.html', classes=classes)

@app.route('/register', methods=['POST'])
def register():
    cur = None
    try:
        
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('index'))  # Assuming a route for the registration page exists

        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM Users WHERE email = %s", (email,))
        if cur.fetchone():
            flash('Email already exists')
            return redirect(url_for('index'))
        else:
            cur.execute("INSERT INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (first_name, last_name, birthdate, email, password, role))
            mysql.connection.commit()

            # Fetch the newly registered user's ID for session setup
            cur.execute("SELECT id, role FROM Users WHERE email = %s", (email,))
            user_data = cur.fetchone()
            session['user_id'] = user_data['id']
            session['role'] = user_data['role']

            flash('Registration successful')
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
    except Exception as e:
        # Log the exception and handle it
        flash('An error occurred during registration. Please try again.')
        return redirect(url_for('register'))
    finally:
        if cur is not None:
            cur.close()
    
@app.route('/login', methods=['POST'])
def login():
    cur = None
    try:
        username = request.form['username']
        raw_password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password, role FROM Users WHERE email = %s", (username,))
        user_data = cur.fetchone()

        if user_data and user_data['password'] == raw_password:
            session['user_id'] = user_data['id']
            session['role'] = user_data['role']
            flash('Login successful')

            # Redirect to the dashboard based on the user's role
            if user_data['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user_data['role'] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:  # Assume student if not admin or teacher
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('index'))  # Assuming you have a route for showing the login page
    except Exception as e:
        # Log the exception and handle it
        flash('An error occurred during login. Please try again.')
        return redirect(url_for('index'))
    finally:
        if cur is not None:
            cur.close()

@app.route('/student-dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return "Unauthorized", 401

    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT Courses.id, Courses.title, Courses.description, COUNT(Assignment.id) as assignment_count
                   FROM Enrollment
                   JOIN Courses ON Enrollment.course_id = Courses.id
                   LEFT JOIN Assignment ON Courses.id = Assignment.course_id
                   WHERE Enrollment.student_id = %s
                   GROUP BY Courses.id''', (user_id,))
    courses = cur.fetchall()
    cur.execute('''SELECT Assignment.title, Assignment.dueDate
                    FROM Assignment
                    JOIN Enrollment ON Enrollment.course_id = Assignment.course_id
                    WHERE Enrollment.student_id = %s''', (user_id,))
    assignments = cur.fetchall()
    cur.close()

    return render_template('webpages/student-dashboard.html', courses=courses, assignments = assignments)

@app.route('/join-class', methods=['POST'])
def join_class():
    if 'user_id' not in session:
        return "Unauthorized", 401

    user_id = session['user_id']
    course_id = request.form['course_id']
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Enrollment (student_id, course_id) VALUES (%s, %s)', (user_id, course_id))
        mysql.connection.commit()
        flash('Successfully joined the class!')
    except Exception as e:
        flash('An error occurred while joining the class.')
        print(e)
    finally:
        cur.close()
    
    return redirect(url_for('student_dashboard'))

@app.route('/select-class')
def select_class():
    if 'user_id' not in session:
        # Redirect to login if not logged in
        return redirect(url_for('login'))

    user_id = session['user_id']
    cur = mysql.connection.cursor()
    # Retrieve distinct courses not yet enrolled by the user
    cur.execute('''
        SELECT DISTINCT Courses.* FROM Courses WHERE id NOT IN (
            SELECT DISTINCT course_id FROM Enrollment WHERE student_id = %s
        )
    ''', (user_id,))
    available_courses = cur.fetchall()
    cur.close()
    print(available_courses)
    return render_template('webpages/select-class.html', courses=available_courses)

@app.route('/student-course')
def student_course():
    return render_template('webpages/student-course.html')

@app.route('/student-grades')
def student_grades():
    return render_template('webpages/student-grades.html')

@app.route('/student-assignment')
def student_assignment():
    assignments = get_assignments()
    return render_template('webpages/student-assignment.html', assignments = assignments)

@app.route('/student-resource')
def student_resource():
    return render_template('webpages/student-resource.html')

@app.route('/quiz')
def quiz():
    return render_template('webpages/quiz.html')

@app.route('/written_assignment')
def written_assignment():
    return render_template('webpages/written-assignment.html')

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

@app.route('/teacher-course')
def teacher_course():
    return render_template('webpages/teacher-course.html')

@app.route('/teacher-grades')
def teacher_grades():
    return render_template('webpages/teacher-grades.html')

@app.route('/teacher-assignment')
def teacher_assignment():
    assignments = get_assignments()
    return render_template('webpages/teacher-assignment.html', assignments = assignments)

@app.route('/teacher-resource')
def teacher_resource():
    return render_template('webpages/teacher-resource.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return "Unauthorized", 401

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Users')
    users = cur.fetchall()
    cur.execute('SELECT * FROM Courses')
    courses = cur.fetchall()
    cur.close()

    return render_template('webpages/admin-dashboard.html', users=users, courses=courses)

@app.route('/admin-course')
def admin_courses():
    return render_template('webpages/admin-courses.html')

# Course details
@app.route('/course-details')
def course_details():
    return render_template('webpages/course-details.html')

# Create course
@app.route('/create-course')
def create_course():
    return render_template('webpages/create-course.html')

# assign teacher
@app.route('/assign-teacher')
def assign_teacher():
    return render_template('webpages/assign-teacher.html')

def get_assignments():
    teacher_id = session.get('user_id')
    if not teacher_id:
        print("User ID not found in session")
        return []

    try:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT Assignment.title, Assignment.description, Assignment.dueDate
                       FROM Assignment
                       JOIN TeacherCourses ON Assignment.course_id = TeacherCourses.course_id
                       WHERE TeacherCourses.teacher_id = %s''', (teacher_id,))
        assignments = cur.fetchall() or []  # Ensure assignments is not None
        cur.close()
        return assignments
    except Exception as e:
        print(f"An error occurred: {e}")
        return []  # Return an empty list on error


@app.route('/create-assignment')
def create_assignment():
    courses = get_teacher_courses()
    return render_template('webpages/create-assignment.html', courses = courses)

def get_teacher_courses():
    teacher_id = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute('''SELECT Courses.title, Courses.id
                   FROM TeacherCourses
                   JOIN Courses ON TeacherCourses.course_id = Courses.id
                   WHERE TeacherCourses.teacher_id = %s''', (teacher_id,))
    courses = cur.fetchall()
    cur.close()

    return courses

@app.route('/submit-assignment', methods=['POST'])
def submit_assignment():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    class_id = request.form['class_id']

    try:
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO Assignment (title, description, dueDate, course_id)
            VALUES (%s, %s, %s, %s)
        ''', (title, description, due_date, class_id))
        mysql.connection.commit()
        assignments = get_assignments()
        return render_template('webpages/teacher-assignment.html', assignments = assignments)
    except Exception as e:
        # Log the detailed error message and traceback
        print("An error occurred:", str(e))
        return render_template('webpages/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
