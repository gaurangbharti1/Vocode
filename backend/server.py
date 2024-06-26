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
        CREATE TABLE IF NOT EXISTS Submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            answers VARCHAR(255),
            assignment_id INT,
            question_id INT,
            student_id INT,
            FOREIGN KEY (question_id) REFERENCES Questions(id),
            FOREIGN KEY (assignment_id) REFERENCES Assignment(id),
            FOREIGN KEY (student_id) REFERENCES Users(id)
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

    cur.execute('''CREATE TABLE IF NOT EXISTS Grade (
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

@app.route('/admin_profile')
def admin_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()

    return render_template('webpages/admin-profile.html', user=user_details)

@app.route('/admin_edit_profile', methods=['GET', 'POST'])
def admin_edit_profile():
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
        return redirect(url_for('admin-profile'))

    # Always fetch the user details to display in the form, for both GET and POST
    cur.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()

    return render_template('webpages/admin-editprofile.html', user=user_details)

@app.route('/teacher-profile')
def teacher_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()

    return render_template('webpages/teacher-profile.html', user=user_details)

@app.route('/teacher-editprofile', methods=['GET', 'POST'])
def teacher_edit_profile():
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
        return redirect(url_for('teacher-profile'))

    # Always fetch the user details to display in the form, for both GET and POST
    cur.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()

    return render_template('webpages/teacher-editprofile.html', user=user_details)


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


@app.route('/student-course/<int:courseid>')
def student_course(courseid):
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
            
    return render_template('webpages/student-course.html', course=course, announcements=announcements)

@app.route('/student-grades/<int:courseid>')
def student_grades(courseid):
    course=get_course(courseid)

    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT Assignment.title, Assignment.description, Assignment.due_date, Grade.grade
        FROM Grade
        JOIN Assignment ON Grade.assignment_id = Assignment.id
        WHERE Grade.student_id = %s AND Assignment.course_id = %s
    ''', (session.get('user_id'), courseid))
    graded_assignments = cur.fetchall()

    return render_template('webpages/student-grades.html', course=course, graded_assignments = graded_assignments)

@app.route('/student-assignment/<int:courseid>')
def student_assignment(courseid):
    course = get_course(courseid)

    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT Assignment.id, Assignment.title, Assignment.description, Assignment.due_Date, Assignment.is_essay
        FROM Assignment
        LEFT JOIN Grade ON Assignment.id = Grade.assignment_id AND Grade.student_id = %s
        WHERE Assignment.course_id = %s AND Grade.grade IS NULL
    ''', (session.get('user_id'), courseid))
    assignments = cur.fetchall()
    cur.close()
    cur.close()

    return render_template('webpages/student-assignment.html', assignments = assignments, course=course)

@app.route('/student-resource/<int:courseid>')
def student_resource(courseid):
    course=get_course(courseid)
    return render_template('webpages/student-resource.html', course=course)

@app.route('/quiz/<int:assignment_id>')
def quiz(assignment_id):
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT q.id AS question_id, q.name AS question_text, a.id AS answer_id, a.name AS answer_text
        FROM Questions q
        JOIN Answers a ON q.id = a.question_id
        WHERE q.assignment_id = %s AND q.is_essay = FALSE
        ORDER BY q.id, a.id
    ''', (assignment_id,))
    result = cur.fetchall()
    cur.close()

    if not result:
        return "No quiz found or no multiple choice questions available.", 404

    # Organize questions and answers
    quiz_data = {}
    for row in result:
        question = quiz_data.setdefault(row['question_id'], {
            'id': row['question_id'],
            'question_text': row['question_text'],
            'answers': []
        })
        question['answers'].append({
            'answer_id': row['answer_id'],
            'answer_text': row['answer_text']
        })

    questions = list(quiz_data.values())
    return render_template('webpages/quiz.html', questions=questions, assignment_id=assignment_id)

@app.route('/student-submit-quiz/<int:assignment_id>', methods=['POST'])
def student_submit_quiz(assignment_id):
    answers = request.form.to_dict()
    total_questions = len(answers)
    score = 0

    cur = mysql.connection.cursor()
    for question_id, answer_id in answers.items():
        cur.execute('SELECT is_correct FROM Answers WHERE id = %s', (answer_id,))
        result = cur.fetchone()
        if result and result['is_correct']:
            score += 1

    grade = (score / total_questions) * 100
        # Insert the new grade
    cur.execute('INSERT INTO Grade (student_id, assignment_id, grade) VALUES (%s, %s, %s)',
                (session.get('user_id'), assignment_id, grade))

    mysql.connection.commit()
    cur.close()

    return render_template('webpages/results.html', score=score, total_questions=total_questions)

@app.route('/essay/<int:assignment_id>')
def essay(assignment_id):
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT q.id AS question_id, q.name AS question_text
        FROM Questions q
        WHERE q.assignment_id = %s AND q.is_essay = TRUE
        ORDER BY q.id
    ''', (assignment_id,))
    result = cur.fetchall()
    cur.close()

    if not result:
        return "No essay questions available for this assignment.", 404

    # Organize essay questions
    questions = [{
        'id': row['question_id'],
        'question_text': row['question_text']
    } for row in result]

    return render_template('webpages/essay.html', questions=questions, assignment_id=assignment_id)

@app.route('/student-submit-essay/<int:assignment_id>', methods=['POST'])
def student_submit_essay(assignment_id):
    cur = mysql.connection.cursor()
    student_id = session.get('user_id')  # Assuming student_id is stored in session

    try:
        for key, value in request.form.items():
            if key.startswith('answer_'):
                question_id = key.split('_')[1]
                # Insert each essay answer into the Submissions table
                cur.execute('''
                    INSERT INTO Submissions (answers, assignment_id, question_id, student_id)
                    VALUES (%s, %s, %s, %s)
                ''', (value, assignment_id, question_id, student_id))
        mysql.connection.commit()
        flash('Your essay responses have been submitted successfully.')
    except Exception as e:
        mysql.connection.rollback()
        flash('An error occurred while submitting your essays.')
        app.logger.error(f"Error submitting essays: {str(e)}")
    finally:
        cur.close()

    return redirect(url_for('student_dashboard'))

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
    if not course:
        return "Course not found", 404

    cur = mysql.connection.cursor()
    try:
        # Fetch assignments and any students who have submitted them
        cur.execute('''
            SELECT a.id, a.title, u.first_name, u.last_name, s.student_id
            FROM Assignment a
            LEFT JOIN Submissions s ON a.id = s.assignment_id
            LEFT JOIN Users u ON s.student_id = u.id
            WHERE a.course_id = %s AND
            a.is_essay = TRUE
            ORDER BY a.id, s.student_id
        ''', (courseid,))
        raw_data = cur.fetchall()
    except Exception as e:
        flash('Failed to fetch assignments and student submissions.')
        app.logger.error(f"Error fetching assignments and submissions: {str(e)}")
        return render_template('webpages/error.html'), 500
    finally:
        cur.close()

    # Organize data by assignments
    assignments = {}
    for item in raw_data:
        if item['id'] not in assignments:
            assignments[item['id']] = {
                'title': item['title'],
                'submissions': []
            }
        if item['student_id']:  # There is a submission
            assignments[item['id']]['submissions'].append({
                'student_name': f"{item['first_name']} {item['last_name']}",
                'student_id': item['student_id']  # Ensure student_id is included
            })

    return render_template('webpages/teacher-grades.html', course=course, assignments=assignments)

@app.route('/review-submission/<int:assignment_id>/<int:student_id>')
def review_submission(assignment_id, student_id):
    cur = mysql.connection.cursor()
    try:
        # Fetch questions and the corresponding student's answers for the assignment
        cur.execute('''
            SELECT q.id, q.name as question_text, s.answers
            FROM Questions q
            LEFT JOIN Submissions s ON q.id = s.question_id AND s.student_id = %s
            WHERE q.assignment_id = %s AND q.is_essay = TRUE
        ''', (student_id, assignment_id))
        submissions = cur.fetchall()
    except Exception as e:
        flash('Failed to fetch submissions for grading.')
        app.logger.error(f"Error fetching submissions: {str(e)}")
        return render_template('webpages/error.html'), 500
    finally:
        cur.close()

    return render_template('webpages/review-submission.html', submissions=submissions, assignment_id=assignment_id, student_id=student_id)

@app.route('/submit-grade/<int:assignment_id>/<int:student_id>', methods=['POST'])
def submit_grade(assignment_id, student_id):
    grade = request.form.get('grade')
    if not grade:
        flash("Please enter a grade.")
        return redirect(url_for('review_submission', assignment_id=assignment_id, student_id=student_id))

    cur = mysql.connection.cursor()
    try:
        # Update or insert the grade into the Grades table
        cur.execute('''
            INSERT INTO Grade (student_id, assignment_id, grade) VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE grade = %s
        ''', (student_id, assignment_id, grade, grade))
        mysql.connection.commit()
        flash('Grade successfully submitted.')
    except Exception as e:
        mysql.connection.rollback()
        flash('Failed to submit grade.')
        app.logger.error(f"Error submitting grade: {str(e)}")
    finally:
        cur.close()

    return redirect(url_for('teacher_dashboard'))

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
        cur.execute('''SELECT Assignment.title, Assignment.description, Assignment.due_date
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
    session['courseid'] = class_id

    try:
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO Assignment (title, description, due_date, is_essay, course_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (title, description, due_date, isEssay, class_id))
        assignment_id = cur.lastrowid
        mysql.connection.commit()

        if isEssay == "0":
            return redirect(url_for('create_quiz', assignment_id=assignment_id, courseid=class_id))
        else:
            return redirect(url_for('create_essay', assignment_id=assignment_id, courseid=class_id))
    except Exception as e:
        # Log the detailed error message and traceback
        print("An error occurred:", str(e))
        return render_template('webpages/500.html'), 500

@app.route('/create-quiz/<int:courseid>/<int:assignment_id>')
def create_quiz(courseid, assignment_id):
    return render_template('webpages/create-quiz.html', assignment_id=assignment_id, courseid=courseid)

@app.route('/create-essay/<int:courseid>/<int:assignment_id>')
def create_essay(courseid, assignment_id):
    return render_template('webpages/create-essay.html', assignment_id=assignment_id, courseid=courseid)


@app.route('/submit-quiz/<int:assignment_id>', methods=['POST'])
def submit_quiz(assignment_id):
    for i in range(1, 4):  # For each question
        question_text = request.form.get(f'question{i}')
        correct_answer_index = request.form.get(f'question{i}_correct')

        # Insert the question
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO Questions (name, is_essay, assignment_id) VALUES (%s, %s, %s)''',
                    (question_text, False, assignment_id))
        question_id = cur.lastrowid  # Get the ID of the inserted question

        for j in range(1, 3):  # For each answer
            answer_text = request.form.get(f'question{i}_answer{j}')
            is_correct = str(j) == correct_answer_index  # Compare strings to see if this is the correct answer

            # Insert the answer
            cur.execute('''INSERT INTO Answers (name, is_correct, question_id) VALUES (%s, %s, %s)''',
                        (answer_text, is_correct, question_id))
        
        mysql.connection.commit()  # Commit after inserting each question and its answers

    cur.close()
    return redirect(url_for('course_details', courseid=session.get('courseid')))

@app.route('/submit-essay/<int:assignment_id>', methods=['POST'])
def submit_essay(assignment_id):
    try:
        cur = mysql.connection.cursor()
        for i in range(1, 4):  # Assuming three essay questions
            essay_question = request.form.get(f'essayQuestion{i}')
            if essay_question:  # Only insert if the question field was filled out
                cur.execute('''INSERT INTO Questions (name, is_essay, assignment_id) VALUES (%s, %s, %s)''',
                            (essay_question, True, assignment_id))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error occurred: {e}")
        return render_template('webpages/500.html'), 500
    finally:
        cur.close()
    
    return redirect(url_for('course_details', courseid=session.get('courseid')))

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
