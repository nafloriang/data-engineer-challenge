from flask import Flask, jsonify, request
import sqlite3
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

# JWT Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

# Initialize JWT Manager
jwt = JWTManager(app)

# Database filename
DATABASE = 'mydatabase.db'

def get_db():
    """Establish a connection to the SQLite database and configure rows to be returned as dictionaries."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def get_user(username):
    """Retrieve user information from the database based on the provided username."""
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

@app.route('/')
def hello_world():
    """Basic route to verify the application is running."""
    return "Welcome to the Globant Challenge Solution"

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    print(f"Provided username: {username}")
    print(f"Provided password: {password}")
    
    user = get_user(username)
    
    if user:
        print(f"Database hash for {username}: {user['password']}")
        hashed_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
        
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            print(f"Password mismatch for {username}.")
    else:
        print("User not found in the database.")
    
    return jsonify({"msg": "Invalid username or password"}), 401

@app.route('/jobs/')
@jwt_required()
def get_jobs():
    """Retrieve all job listings from the database."""
    conn = get_db()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return jsonify(jobs)

@app.route('/departments/')
@jwt_required()
def get_departments():
    """Retrieve all department listings from the database."""
    conn = get_db()
    departments = conn.execute('SELECT * FROM departments').fetchall()
    conn.close()
    return jsonify(departments)

@app.route('/hired_employees/')
@jwt_required()
def get_hired_employees():
    """Retrieve all hired employees from the database."""
    conn = get_db()
    hired_employees = conn.execute('SELECT * FROM hired_employees').fetchall()
    conn.close()
    return jsonify(hired_employees)

if __name__ == "__main__":
    app.run(debug=True)
