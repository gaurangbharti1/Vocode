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

@app.route('/test')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
    cur.execute("INSERT INTO example VALUES (1, 'Hello')")

    cur.execute("SELECT * FROM example")
    results = cur.fetchall()
    print(results)
    mysql.connection.commit()
    return jsonify({'message': 'Hello, World!'})

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