from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import datetime

app = Flask(__name__, template_folder='../frontend/', static_url_path='', static_folder='../frontend')

app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql3698588'
app.config['MYSQL_PASSWORD'] = 'CYCutPr556'
app.config['MYSQL_DB'] = 'sql3698588'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'test_key'

bcrypt = Bcrypt(app)
mysql = MySQL(app)
@app.before_request
def initialize_database():
    cur = mysql.connection.cursor()

    # Create tables with proper datatype and constraint definitions
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            date_of_birth DATE,
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            role ENUM('admin', 'teacher', 'student')
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            admin_id INT,
            FOREIGN KEY (admin_id) REFERENCES Users(id)
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS CourseDetails (
            course_id INT,
            code VARCHAR(10) UNIQUE,
            start_date DATE,
            end_date DATE,
            seats INT,
            PRIMARY KEY (course_id),
            FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Assignment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            due_date DATE,
            is_essay BOOLEAN,
            course_id INT,
            FOREIGN KEY (course_id) REFERENCES Courses(id)
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            is_essay BOOLEAN,
            assignment_id INT,
            FOREIGN KEY (assignment_id) REFERENCES Assignment(id)
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Answers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            is_correct BOOLEAN,
            question_id INT,
            FOREIGN KEY (question_id) REFERENCES Questions(id)
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Announcements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            date DATETIME,
            course_id INT,
            FOREIGN KEY (course_id) REFERENCES Courses(id)
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Enrollment (
            student_id INT,
            course_id INT,
            is_approved TINYINT DEFAULT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Users(id),
            FOREIGN KEY (course_id) REFERENCES Courses(id)
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            student_id INT,
            assignment_id INT,
            grade INT,
            PRIMARY KEY (student_id, assignment_id),
            FOREIGN KEY (student_id) REFERENCES Users(id),
            FOREIGN KEY (assignment_id) REFERENCES Assignment(id)
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS TeacherCourses (
            teacher_id INT,
            course_id INT,
            PRIMARY KEY (teacher_id, course_id),
            FOREIGN KEY (teacher_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
        )''')

    # Insert default records only if they do not exist
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('John', 'Doe', '1990-01-01', 'john.doe@example.com', 'hashed_password', 'admin')")
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jane', 'Smith', '1992-02-02', 'jane.smith@example.com', 'hashed_password', 'teacher')")
    cur.execute("INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jim', 'Bean', '1994-03-03', 'jim.bean@example.com', 'hashed_password', 'student')")

    # Insert courses
    cur.execute("INSERT IGNORE INTO Courses (title, description, admin_id) VALUES ('Introduction to Python', 'Beginner-friendly course on Python.', 1)")
    cur.execute("INSERT IGNORE INTO Courses (title, description, admin_id) VALUES ('Web Design Basics', 'Learn HTML, CSS, and JavaScript.', 1)")
    cur.execute("INSERT IGNORE INTO Courses (title, description, admin_id) VALUES ('Data Structures', 'Advanced course on data organizing techniques.', 1)")

    # Insert course details
    cur.execute("INSERT IGNORE INTO CourseDetails (course_id, code, start_date, end_date, seats) VALUES (1, 'PY101', '2023-01-01', '2023-06-01', 30)")
    cur.execute("INSERT IGNORE INTO CourseDetails (course_id, code, start_date, end_date, seats) VALUES (2, 'WD101', '2023-02-01', '2023-07-01', 30)")
    cur.execute("INSERT IGNORE INTO CourseDetails (course_id, code, start_date, end_date, seats) VALUES (3, 'DS101', '2023-03-01', '2023-08-01', 30)")

    # Enroll the student with different approval statuses
    cur.execute("INSERT IGNORE INTO Enrollment (student_id, course_id, is_approved) VALUES (3, 1, 1)")  # Approved
    cur.execute("INSERT IGNORE INTO Enrollment (student_id, course_id, is_approved) VALUES (3, 2, NULL)")  # Pending
    cur.execute("INSERT IGNORE INTO Enrollment (student_id, course_id, is_approved) VALUES (3, 3, 0)")  # Rejected

    cur.execute("INSERT IGNORE INTO TeacherCourses (teacher_id, course_id) VALUES (2, 1)")
    cur.execute("INSERT IGNORE INTO TeacherCourses (teacher_id, course_id) VALUES (2, 2)")

    mysql.connection.commit()
    cur.close()
    print('Database initialized.')

@app.before_request
def initialize_assignments():
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) AS count FROM Assignment")
    result = cur.fetchone()
    if result['count'] == 0:
        cur.execute("INSERT INTO Assignment (title, description, due_date, is_essay, course_id) VALUES ('Introduction to Web Development', 'Complete the HTML and CSS exercise.', '2024-05-01', 1, 1)")
        cur.execute("INSERT INTO Assignment (title, description, due_date, is_essay, course_id) VALUES ('Advanced Database Management', 'Read chapter 4 of the database textbook and answer questions 1-10.', '2024-06-30', 0, 2)")
        mysql.connection.commit()
        print("Assignments inserted.")
    else:
        print("Assignments table was not empty")

    cur.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('webpages/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('webpages/500.html'), 500


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

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        new_first_name = request.form.get('first_name')
        new_last_name = request.form.get('last_name')
        new_email = request.form.get('new_email')
        curr_password = request.form.get('curr_password')
        new_password = request.form.get('new_password')

        cur.execute('SELECT password FROM Users WHERE id = %s', (user_id,))
        user_data = cur.fetchone()

        if new_first_name:
            cur.execute('UPDATE Users SET first_name = %s WHERE id = %s', (new_first_name, user_id))
        if new_last_name:
            cur.execute('UPDATE Users SET last_name = %s WHERE id = %s', (new_last_name, user_id))
        if new_email:
            cur.execute('UPDATE Users SET email = %s WHERE id = %s', (new_email, user_id))
        if new_password:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            cur.execute('UPDATE Users SET password = %s WHERE id = %s', (hashed_password, user_id))
        mysql.connection.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))
    
    # Always fetch the user details to display in the form, for both GET and POST
    cur.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()

    return render_template('webpages/edit-profile.html', user=user_details)

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
@app.route('/enroll-course', methods=['POST'])
def enroll_course():
    if 'user_id' not in session or session['role'] != 'student':
        return "Unauthorized", 401

    course_code = request.form.get('course_code')
    student_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute("SELECT course_id FROM CourseDetails WHERE code = %s", [course_code])
    course_detail = cur.fetchone()

    if course_detail:
        cur.execute("INSERT INTO Enrollment (student_id, course_id, is_approved) VALUES (%s, %s, NULL)", (student_id, course_detail['course_id']))
        mysql.connection.commit()
        flash("Enrollment request sent. Waiting for admin approval.")
    else:
        flash("Course code not found.", "error")

    cur.close()
    return redirect(url_for('student_dashboard'))


@app.route('/admin-review-enrollments')
def admin_review_enrollments():
    if 'user_id' not in session or session['role'] != 'admin':
        return "Unauthorized", 401

    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT Enrollment.student_id, Users.first_name, Users.last_name, Courses.title, CourseDetails.code, Enrollment.course_id
        FROM Enrollment
        JOIN Users ON Enrollment.student_id = Users.id
        JOIN Courses ON Enrollment.course_id = Courses.id
        JOIN CourseDetails ON Courses.id = CourseDetails.course_id
        WHERE Enrollment.is_approved IS NULL
    ''')
    pending_enrollments = cur.fetchall()
    cur.close()

    return render_template('webpages/admin-review-enrollments.html', enrollments=pending_enrollments)

@app.route('/admin-approve-reject', methods=['POST'])
def admin_approve_reject():
    enrollment_id = request.form.get('enrollment_id')
    decision = request.form.get('decision')  # 'approve' or 'reject'
    
    cur = mysql.connection.cursor()
    status = 1 if decision == 'approve' else 0 if decision == 'reject' else None
    cur.execute("UPDATE Enrollment SET is_approved = %s WHERE student_id = %s AND course_id = %s", (status, *enrollment_id.split("-")))
    mysql.connection.commit()
    flash("Enrollment decision updated successfully.")
    cur.close()

    return redirect(url_for('admin_review_enrollments'))



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
            return render_template('webpages/error.html', error_message='Passwords do not match.', return_url=url_for('index'))
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM Users WHERE email = %s", (email,))
        if cur.fetchone():
            return render_template('webpages/error.html', error_message='Email already exists.', return_url=url_for('index'))
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
        return render_template('webpages/error.html', error_message='An error occurred during registration. Please try again.', return_url=url_for('index'))
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
            return render_template('webpages/error.html', error_message='Invalid username or password.', return_url=url_for('index'))
    except Exception as e:
        # Log the exception and handle it
        return render_template('webpages/error.html', error_message='An error occurred during login. Please try again.', return_url=url_for('index'))
    finally:
        if cur is not None:
            cur.close()

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

@app.route('/admin-courses')
def admin_courses():
    cur = mysql.connection.cursor()
    # Join Courses with CourseDetails and Users to fetch course information along with the instructor's name
    cur.execute('''
        SELECT Courses.title, CourseDetails.start_date, CourseDetails.end_date, 
               CourseDetails.seats, Users.first_name, Users.last_name,
               (SELECT COUNT(*) FROM Enrollment WHERE course_id = Courses.id) as seats_filled
        FROM Courses
        JOIN CourseDetails ON Courses.id = CourseDetails.course_id
        JOIN Users ON Courses.admin_id = Users.id
    ''')
    courses_raw = cur.fetchall()
    cur.close()
    
    courses = []
    for course in courses_raw:
        # Check if dates are not None and directly assign them; otherwise, provide a default value
        start_date = course['start_date'] if course['start_date'] else 'N/A'
        end_date = course['end_date'] if course['end_date'] else 'N/A'
        
        course_data = {
            'title': course['title'],
            'start_date': start_date,
            'end_date': end_date,
            'seats': course['seats'],
            'seats_filled': course['seats_filled'],
            'professor': f"{course['first_name']} {course['last_name']}"
        }
        courses.append(course_data)

    return render_template('webpages/admin-courses.html', courses=courses)

@app.route('/create-course-form')
def create_course_form():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    return render_template('webpages/create-course-form.html')

@app.route('/create-course', methods=['POST'])
def create_course():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    title = request.form.get('course-name', '').strip()
    course_code = request.form.get('course-code', '').strip()
    description = request.form.get('course-description', '').strip()
    start_date = request.form.get('start-date')
    end_date = request.form.get('end-date')
    seats = request.form.get('seats', '0')
    professor_id = request.form.get('professor-id')  # Assuming the professor ID is passed from the form

    # Basic validation
    if not title or not description or not start_date or not end_date or not seats.isdigit() or int(seats) < 1 or not professor_id.isdigit():
        flash('Invalid input data. Please ensure all fields are correctly filled.', 'error')
        return redirect(url_for('create_course_form'))

    try:
        cur = mysql.connection.cursor()
        # Insert the new course into the Courses table
        cur.execute('''INSERT INTO Courses (title, description, admin_id) 
                       VALUES (%s, %s, %s)''',
                    (title, description, session['user_id']))
        course_id = cur.lastrowid  # Retrieve the auto-generated course_id

        # Insert the course details into the CourseDetails table
        cur.execute('''INSERT INTO CourseDetails (course_id, code, start_date, end_date, seats) 
                       VALUES (%s, %s, %s, %s, %s)''',
                    (course_id,course_code, start_date, end_date, int(seats)))

        # Assign the course to the professor using the TeacherCourses table
        cur.execute('''INSERT INTO TeacherCourses (teacher_id, course_id) 
                       VALUES (%s, %s)''',
                    (professor_id, course_id))

        mysql.connection.commit()
        flash('Course created and professor assigned successfully.')
    except Exception as e:
        mysql.connection.rollback()
        flash('Failed to create course. Please try again.')
        print(e)  # For debugging purposes
    finally:
        cur.close()

    return redirect(url_for('admin_dashboard'))
@app.route('/student-dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return "Unauthorized", 401

    user_id = session['user_id']
    cur = mysql.connection.cursor()
    # Fetch courses and their approval status
    cur.execute('''
        SELECT Courses.id, Courses.title, Courses.description, CourseDetails.code, Enrollment.is_approved
        FROM Enrollment
        JOIN Courses ON Enrollment.course_id = Courses.id
        JOIN CourseDetails ON Courses.id = CourseDetails.course_id
        WHERE Enrollment.student_id = %s
    ''', (user_id,))
    courses = cur.fetchall()

    # Fetch assignments for courses where the student's enrollment is approved
    cur.execute('''
        SELECT Assignment.title, Assignment.due_date
        FROM Assignment
        JOIN Courses ON Assignment.course_id = Courses.id
        JOIN Enrollment ON Courses.id = Enrollment.course_id
        WHERE Enrollment.student_id = %s AND Enrollment.is_approved = 1
    ''', (user_id,))
    assignments = cur.fetchall()
    cur.close()

    return render_template('webpages/student-dashboard.html', courses=courses, assignments=assignments)


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

@app.route('/teacher-grades/<int:courseid>')
def teacher_grades(courseid):
    course = get_course(courseid)
    return render_template('webpages/teacher-grades.html', course=course)

@app.route('/teacher-assignment/<int:courseid>')
def teacher_assignment(courseid):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Assignment WHERE course_id = %s", [courseid])
    assignments = cur.fetchall()
    cur.close()
    
    course = get_course(courseid)
    return render_template('webpages/teacher-assignment.html', assignments = assignments, course=course)

@app.route('/teacher-resource/<int:courseid>')
def teacher_resource(courseid):
    course = get_course(courseid)
    return render_template('webpages/teacher-resource.html', course=course)

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

def get_course(courseid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Courses WHERE id = %s", [courseid])
    course = cur.fetchone()
    cur.close()

    return course

@app.route('/course-details/<int:courseid>')
def course_details(courseid):
    course = get_course(courseid)
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Announcements WHERE course_id = %s ORDER BY date DESC", [courseid])
        announcements = cur.fetchall()
    except Exception as e:
        print("Failed to fetch announcements:", str(e))
        announcements = []
    finally:
        if cur:
            cur.close()
            
    return render_template('webpages/teacher-course.html', course=course, announcements=announcements)

@app.route('/create-announcement/<int:courseid>')
def create_announcement(courseid):
    course = get_course(courseid)
    return render_template('webpages/create-announcement.html', course=course)

@app.route('/create-assignment/<int:courseid>')
def create_assignment(courseid):
    courses = get_teacher_courses()
    course = get_course(courseid)
    return render_template('webpages/create-assignment.html', courses = courses, course=course)

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
    isEssay = request.form['assignment_type']

    try:
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO Assignment (title, description, dueDate, isEssay, course_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (title, description, due_date, isEssay, class_id))
        mysql.connection.commit()
        return redirect(url_for('teacher_assignment', courseid=class_id))
    except Exception as e:
        # Log the detailed error message and traceback
        print("An error occurred:", str(e))
        return render_template('webpages/500.html'), 500

@app.route('/submit-announcement', methods=['POST'])
def submit_announcement():
    title = request.form['title']
    description = request.form['description']
    class_id = request.form['courseId']
    course = get_course(class_id)
    current_datetime = datetime.datetime.now()
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO Announcements (title, description, date, course_id)
            VALUES (%s, %s, %s, %s)
        ''', (title, description, current_datetime, class_id))
        mysql.connection.commit()
        return redirect(url_for('course_details', courseid=class_id))
    except Exception as e:
        # Log the detailed error message and traceback
        print("An error occurred:", str(e))
        return render_template('webpages/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
