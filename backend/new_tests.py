import unittest
from server import app, bcrypt
from flask import json

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.email = 'testuser@example.com'
        self.password = 'testpassword'

    def register_user(self, email, password, role='student'):
        return self.app.post('/register', data={
            'firstname': 'Test',
            'lastname': 'User',
            'birthdate': '2000-01-01',
            'email': email,
            'password': password,
            'confirm_password': password,
            'role': role
        })

    def login_user(self, email, password):
        return self.app.post('/login', data={
            'username': email,
            'password': password
        })

    def test_register(self):
        response = self.register_user(self.email, self.password)
        # Check for redirect status code instead of flash message
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        # Ensure the user is registered before attempting to login
        self.register_user(self.email, self.password)
        response = self.login_user(self.email, self.password)
        # Check for redirect status code instead of flash message
        self.assertEqual(response.status_code, 302)
        self.assertIn('/student-dashboard', response.data.decode()) 
        
    def test_access_profile_unauthorized(self):
        # Attempt to access the profile without logging in
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 302)  # Assuming a redirect to login page for unauthorized access

    def test_access_profile_authorized(self):
        self.register_user('authorized@example.com', self.password)
        self.login_user('authorized@example.com', self.password)
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)  # Success if logged in

    def test_assignments_access(self):
        self.register_user('assignmentuser@example.com', self.password, 'student')
        self.login_user('assignmentuser@example.com', self.password)
        response = self.app.get('/assignments')
        self.assertEqual(response.status_code, 200)  # Ensure the assignments page is accessible for logged-in users

    def test_teacher_dashboard_access(self):
        self.register_user('teacheruser@example.com', self.password, 'teacher')
        self.login_user('teacheruser@example.com', self.password)
        response = self.app.get('/teacher-dashboard')
        self.assertEqual(response.status_code, 200)  # Teachers should be able to access their dashboard

    def test_student_dashboard_access(self):
        self.register_user('studentuser@example.com', self.password, 'student')
        self.login_user('studentuser@example.com', self.password)
        response = self.app.get('/student-dashboard')
        self.assertEqual(response.status_code, 200)  # Students should be able to access their dashboard

    def test_unauthorized_access_to_teacher_dashboard(self):
        self.register_user('unauthuser@example.com', self.password, 'student')
        self.login_user('unauthuser@example.com', self.password)
        response = self.app.get('/teacher-dashboard')
        self.assertNotEqual(response.status_code, 200)  # Unauthorized users should not access the teacher dashboard

    # You can continue adding more tests for other endpoints and functionalities, including error cases and validation checks.

if __name__ == '__main__':
    unittest.main()
