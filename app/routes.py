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
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = get_user(username)
    
    if user:
        hashed_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
        
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            return jsonify({"msg": "Invalid username or password"}), 401
    else:
        return jsonify({"msg": "Invalid username or password"}), 401

@routes.route('/jobs/')
@jwt_required()
def get_jobs():
    conn = get_db()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return jsonify([dict(job) for job in jobs])

@routes.route('/departments/')
@jwt_required()
def get_departments():
    conn = get_db()
    departments = conn.execute('SELECT * FROM departments').fetchall()
    conn.close()
    return jsonify([dict(department) for department in departments])

@routes.route('/hired_employees/')
@jwt_required()
def get_hired_employees():
    conn = get_db()
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

@routes.route('/insert/<string:table_name>', methods=['POST'])
@jwt_required()
def insert_data(table_name):
    if table_name not in ['hired_employees', 'jobs', 'departments']:
        return jsonify({"message": "Invalid table name"}), 400

    data = request.json.get('data')

    if not isinstance(data, list) or len(data) > 1000:
        return jsonify({"message": "Data must be a list of 1 to 1000 records"}), 400

    conn = get_db()
    cursor = conn.cursor()

    if table_name == 'hired_employees':
        for record in data:
            if 'name' in record:
                cursor.execute("INSERT INTO hired_employees (name, datetime, department_id, job_id) VALUES (?, ?, ?, ?)", 
                               (record.get('name'), record.get('datetime'), record.get('department_id'), record.get('job_id')))

    elif table_name == 'jobs':
        for record in data:
            if 'job' in record:
                cursor.execute("INSERT INTO jobs (job) VALUES (?)", 
                               (record.get('job'),))

    elif table_name == 'departments':
        for record in data:
            if 'department' in record:
                cursor.execute("INSERT INTO departments (department) VALUES (?)", 
                               (record.get('department'),))
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Insertion successful"}), 200

@routes.route('/metrics/employees_by_job_and_department', methods=['GET'])
@jwt_required()
def employees_by_job_and_department():
    conn = get_db()
    
    # Consulta SQL para el Requisito 1
    query = """
  SELECT 
    departments.Department, 
    jobs.Job,
    SUM(CASE WHEN strftime('%m', Datetime) BETWEEN '01' AND '03' THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN strftime('%m', Datetime) BETWEEN '04' AND '06' THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN strftime('%m', Datetime) BETWEEN '07' AND '09' THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN strftime('%m', Datetime) BETWEEN '10' AND '12' THEN 1 ELSE 0 END) AS Q4
FROM 
    hired_employees
    JOIN departments ON hired_employees.department_id = departments.Id
    JOIN jobs ON hired_employees.job_id = jobs.Id
WHERE 
    strftime('%Y', Datetime) = '2021'
GROUP BY 
    departments.Department, jobs.Job
ORDER BY 
    departments.Department ASC, jobs.Job ASC;
    """
    result = conn.execute(query).fetchall()
    conn.close()

    response = []
    for row in result:
        response.append({
            'department': row['department'],
            'job': row['job'],
            'Q1': row['Q1'],
            'Q2': row['Q2'],
            'Q3': row['Q3'],
            'Q4': row['Q4']
        })

    return jsonify(response)

@routes.route('/metrics/department_hiring_above_average', methods=['GET'])
@jwt_required()
def department_hiring_above_average():
    conn = get_db()
    
    # Consulta SQL para el Requisito 2
    query = """
   SELECT departments.Id AS id, departments.Department AS department, COUNT(hired_employees.id) AS hired
FROM hired_employees
JOIN departments ON hired_employees.department_id = departments.id
WHERE strftime('%Y', Datetime) = '2021'
GROUP BY departments.Id, departments.Department
HAVING hired > (SELECT AVG(employee_count) FROM 
                    (SELECT COUNT(hired_employees.id) AS employee_count
                    FROM hired_employees
                    WHERE strftime('%Y', Datetime) = '2021'
                    GROUP BY hired_employees.department_id) AS avg_table)
ORDER BY hired DESC;
    """
    result = conn.execute(query).fetchall()
    conn.close()

    response = []
    for row in result:
        response.append({
            'id': row['department'],
            'department': row['department'],
            'hired': row['hired']
        })

    return jsonify(response)


