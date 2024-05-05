# Vocode

**Walkthrough Video:** [View Walkthrough](https://youtu.be/tJEbzTNg5TM)

**A step-by-step guide to handling our project:**

- Clone the repository: git clone https://github.com/gaurangbharti1/Vocode.git
- Make sure to have all dependencies installed:
- pip install flask
- pip install mysqldb
- pip install bcrypt
- Run the program: python backend/server.py
- Admin user: john.doe@example.com
- Admin Password: hashed_password
- Teacher user: john.doe@example.com
- Teacher Password: hashed_password
- Student user: john.doe@example.com
- Student Password: hashed_password

**User Requirements:**

1. Course Interaction<br>
   a. Browse and enroll in courses with enrollment confirmation.<br>
   b. View course history and active enrollments.<br>
2. Registration & Login<br>
   a. Secure account creation for students with email verification.<br>
   b. Password reset and user authentication mechanisms.<br>
3. Assignment Handling<br>
   a. Upload functionality for assignment submissions with immediate confirmation.<br>
   b. Access to past submissions and downloadable submission receipts.<br>
4. Feedback System<br>
   a. Display of assignment grades and teacher feedback in student profiles.<br>
   b. Notifications to students upon the release of new grades.<br>
5. Content Creation<br>
   a. Tools for teachers to create and manage various assignment types.<br>
   b. Assignment detail customization including due dates and resources.<br>
6. Course Administration<br>
   a. Interface for admins to create and detail new courses.<br>
   b. Enrollment management with approval/rejection capabilities.<br>

**Functional Requirements:**

USERS-login/signup, update user details.<br>
1.1 System should present a web interface that allows users to register or log in for the platform<br>
1.2 System should have a page to update user details and password<br>
ADMIN-create courses<br>
2.1 System should present an interface for admin users to create courses, with fields to enter a title and description<br>
ADMIN-accepts students for course<br>
3.1 System should present an interface for admin users to be notified that a student wants to register for a course and for the student to be accepted into the course<br>
TEACHER-create different assignments (quizzes and essays)<br>
4.1 System should present an interface for teachers to create assignments with fields to enter a title, assignment type, content (a file and/or description), and a start time and deadline<br>
STUDENT-Enroll in the course<br>
5.1 System should present an interface for students to be able to search for an enroll into a course<br>
STUDENT-submit assignments<br>
6.1 System should present an interface for students to be able to submit an assignment by uploading a file<br>
TEACHER-grade assignments<br>
7.1 System should present an interface for teachers to access each student’s submissions for grading and to provide written feedback<br>
STUDENT-see grades<br>
8.1 System should present an interface for students to be able to view their grades and feedback for an individual assignment <br>
8.2 System should present an interface for students to view a summary of all their assignments for a given course, as well as their overall grade<br>

**Non-functional Requirements:**

The website must be appealing to the user<br>
The platform should load user dashboards within 2 seconds.<br>
Assignment submissions should be processed within 3 seconds.<br>
The system should have an uptime of 99.9%.<br>
The user interface should be intuitive and require minimal training for new users.<br>
The platform should be accessible through the latest versions of major web browsers.<br>

## A Brief Description of the Software

The software is an e-learning platform designed to facilitate educational interactions between students and teachers. It allows for the creation, management, and grading of assignments, enrollment in courses, and dissemination of course materials. The platform serves as a virtual classroom where teachers can post assignments, quizzes, and resources, while students can submit work and view their grades.

**User Group: Students**

- **Scenario: Course Enrollment**  
  A student logs in and enters the course they would like to join. They select a course, and submit an enrollment request.

- **Scenario: Assignment Submission**  
  Once enrolled, a student receives a notification about a new essay assignment. They complete the essay on the platform itself, and submit it through the platform's submission system.

- **Scenario: Grade Review**  
  After assignments have been graded, the student checks their grade and for the essay, and reviews their overall course progress in the gradebook section.

- **Scenario: Material Access**  
  The student accesses the course material section to download lecture slides and notes posted by the teacher for upcoming classes.

- **Scenario: Quiz Participation**  
  The student takes part in a timed quiz posted by the teacher, answering multiple-choice questions on the platform itself before the deadline and their grade for the quiz is available right away.

**User Group: Teachers**

- **Scenario: Assignment Creation**  
  A teacher creates a new multiple-choice quiz, setting questions, possible answers, marking the correct ones, and publishing the quiz for students.

- **Scenario: Essay Assignment Setup**  
  The teacher sets up an essay assignment, providing a detailed question and instructions, setting a due date, and making the assignment available to students.

- **Scenario: Grading**  
  After the deadline, the teacher grades the submitted assignments, providing scores and feedback, which are then made available to students on their dashboards.

- **Scenario: Course Material Upload**  
  The teacher uploads additional reading material and resources for the course, categorizing them by week and lecture topic.

**User Group: Administrators**

- **Scenario: Course Setup**  
  An admin sets up a new course in the system, defining its description, and making it available for teacher assignment and student enrollment.

- **Scenario: Enrollment Approval**  
  The admin reviews and processes enrollment requests from students, and either grants or rejects access to the course.

- **Scenario: User Management**  
  The admin creates user accounts for new teachers, assigning them credentials and linking them with their respective courses.

**Final List of Requirements**

- **User Authentication**  
  Secure login for students, teachers, and administrators. Password recovery and user account management.

- **Course Management**  
  Ability for admins to create, modify, and delete courses. Enrollment control for admins to add or remove students and teachers from courses.

- **Assignment Management**  
  Creation of various assignment types (essays, quizzes) by teachers. Submission functionality for students to turn in assignments.

- **Grading interface**  
  For teachers to evaluate and provide feedback on submissions.

- **Quiz Creation**  
  Dynamic quiz creation tool for teachers to set up multiple-choice questions with designated correct answers. Auto-grading capability based on the predefined answers.

- **Resource Distribution**  
  Platform capability for teachers to upload and share course materials. Download access for students to retrieve course materials.

- **Gradebook**  
  A system for teachers to record and publish grades. Access for students to view their grades and feedback.

- **Notifications and Announcements**  
  In-platform notifications for new assignments, grades, and announcements. Announcement feature for teachers to post important updates.

- **Performance and Scalability**  
  The platform should handle a significant number of simultaneous users without performance degradation. Scalable architecture to add more features like forums, live lectures, etc.
