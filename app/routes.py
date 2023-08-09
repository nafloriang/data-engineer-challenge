from flask import Blueprint, jsonify, request
import bcrypt
from .models import get_user
from .database import get_db
from flask_jwt_extended import jwt_required, create_access_token
from .utils import backup_database, restore_database

# Crear un Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def hello_world():
    return "Welcome to the Globant Challenge Solution"

@routes.route('/login', methods=['POST'])
def login():
    # Extraer datos del request
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Debug logs (opcional)
    print(f"Provided username: {username}")
    print(f"Provided password: {password}")
    
    # Consultar usuario en la base de datos
    user = get_user(username)
    
    if user:
        # Comparar contraseñas
        print(f"Database hash for {username}: {user['password']}")
        hashed_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
        
        # Validar contraseñas y generar token si es correcta
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            print(f"Password mismatch for {username}.")
    else:
        print("User not found in the database.")
    
    return jsonify({"msg": "Invalid username or password"}), 401

@routes.route('/jobs/')
@jwt_required()
def get_jobs():
    # Conectar a la base de datos
    conn = get_db()
    
    # Consultar trabajos
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    
    return jsonify([dict(job) for job in jobs])

@routes.route('/departments/')
@jwt_required()
def get_departments():
    # Conectar a la base de datos
    conn = get_db()
    
    # Consultar departamentos
    departments = conn.execute('SELECT * FROM departments').fetchall()
    conn.close()
    
    return jsonify([dict(department) for department in departments])

@routes.route('/hired_employees/')
@jwt_required()
def get_hired_employees():
    # Conectar a la base de datos
    conn = get_db()
    
    # Consultar empleados contratados
    hired_employees = conn.execute('SELECT * FROM hired_employees').fetchall()
    conn.close()
    
    return jsonify([dict(employee) for employee in hired_employees])

@routes.route('/backup', methods=['POST'])
@jwt_required()
def backup():
    if backup_database():
        return jsonify({"message": "Backup successful"}), 200
    else:
        return jsonify({"message": "Backup failed"}), 500

@routes.route('/restore', methods=['POST'])
@jwt_required()
def restore():
    if restore_database():
        return jsonify({"message": "Restoration successful"}), 200
    else:
        return jsonify({"message": "Restoration failed"}), 500
