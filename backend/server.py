from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import datetime

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

    # Create the Assignments table
    cur.execute('''CREATE TABLE IF NOT EXISTS Assignment (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        description VARCHAR(255),
        dueDate DATE,
        isEssay BOOLEAN,
        course_id INT,
        FOREIGN KEY (course_id) REFERENCES Courses(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        IsEssay BOOLEAN,
        AssignmentID INT,
        FOREIGN KEY (AssignmentID) REFERENCES Assignment(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Answers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        IsCorrect BOOLEAN,
        QuestionID INT,
        FOREIGN KEY (QuestionID) REFERENCES Questions(id)
    )''')


    cur.execute('''CREATE TABLE IF NOT EXISTS Announcements (
        AID INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        description VARCHAR(255),
        date DATETIME,
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
    cur.execute(f"INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('John', 'Doe', '1990-01-01', 'john.doe@example.com', 'hashed_password', 'admin')")
    cur.execute(f"INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jane', 'Smith', '1992-02-02', 'jane.smith@example.com', 'hashed_password', 'teacher')")
    cur.execute(f"INSERT IGNORE INTO Users (first_name, last_name, date_of_birth, email, password, role) VALUES ('Jim', 'Bean', '1994-03-03', 'w', 'hashed_password', 'student')")
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
    #insert dummy questions and answers
    cur.execute("INSERT IGNORE INTO Questions (name, IsEssay, AssignmentID) VALUES ('What is HTML?', 1, 1)")
    cur.execute("INSERT IGNORE INTO Questions (name, IsEssay, AssignmentID) VALUES ('What is SQL?', 0, 2)")
    cur.execute("INSERT IGNORE INTO Answers (name, isCorrect, QuestionID) VALUES ('banana', 0, 2)")
    cur.execute("INSERT IGNORE INTO Answers (name, isCorrect, QuestionID) VALUES ('Structured Query Language', 1, 2)")
    cur.execute("INSERT IGNORE INTO Answers (name, isCorrect, QuestionID) VALUES ('apple', 0, 2)")


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
        cur.execute("INSERT INTO Assignment (title, description, dueDate, isEssay, course_id) VALUES ('Introduction to Web Development', 'Complete the HTML and CSS exercise.', '2024-05-01', 1, 1)")
        cur.execute("INSERT INTO Assignment (title, description, dueDate, isEssay, course_id) VALUES ('Advanced Database Management', 'Read chapter 4 of the database textbook and answer questions 1-10.', '2024-06-30', 0, 2)")

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

# @app.route('/edit_profile')
# def edit_profile():
#     return render_template('webpages/edit-profile.html')

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
    session['courseid'] = class_id

    try:
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO Assignment (title, description, dueDate, isEssay, course_id)
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

@app.route('/submit-quiz/<int:assignment_id>', methods=['POST'])
def submit_quiz(assignment_id):
    for i in range(1, 4):  # For each question
        question_text = request.form.get(f'question{i}')
        correct_answer_index = request.form.get(f'question{i}_correct')

        # Insert the question
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO Questions (name, IsEssay, AssignmentID) VALUES (%s, %s, %s)''',
                    (question_text, False, assignment_id))
        question_id = cur.lastrowid  # Get the ID of the inserted question

        for j in range(1, 3):  # For each answer
            answer_text = request.form.get(f'question{i}_answer{j}')
            is_correct = str(j) == correct_answer_index  # Compare strings to see if this is the correct answer

            # Insert the answer
            cur.execute('''INSERT INTO Answers (name, IsCorrect, QuestionID) VALUES (%s, %s, %s)''',
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
                cur.execute('''INSERT INTO Questions (name, IsEssay, AssignmentID) VALUES (%s, %s, %s)''',
                            (essay_question, True, assignment_id))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error occurred: {e}")
        return render_template('webpages/500.html'), 500
    finally:
        cur.close()
    
    return redirect(url_for('course_details', courseid=session.get('courseid')))

if __name__ == '__main__':
    app.run(debug=True)
