import json
from flask_testing import TestCase
from server import app

class FlaskTestCase(TestCase):

    def create_app(self):
        # Configure the Flask app for testing
        app.config['TESTING'] = True
        return app

    def test_index(self):
        # Test the index route
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World!', response.data)

    def test_register(self):
        # Test the register route
        response = self.client.post('/register', data=json.dumps({'username': 'user3', 'password': 'pass3'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_login(self):
        # Test the login route with correct credentials
        response = self.client.post('/login', data=json.dumps({'username': 'user1', 'password': 'pass1'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

        # Test the login route with incorrect credentials
        response = self.client.post('/login', data=json.dumps({'username': 'user1', 'password': 'wrongpass'}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)

    def test_get_posts(self):
        # Test the posts route
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post 1', response.data)
        self.assertIn(b'Post 2', response.data)

if __name__ == '__main__':
    import unittest
    unittest.main()
