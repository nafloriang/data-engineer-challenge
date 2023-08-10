import sqlite3
import csv
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('mydatabase.db')  
cursor = conn.cursor()

# Función para cargar datos de empleados
def load_hired_employees():
    with open('hired_employees.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            employee_id = int(row[0])
            name = row[1]
            datetime_str = row[2]
            department_id = int(row[3]) if row[3] else None
            job_id = int(row[4]) if row[4] else None
            
            # Convertir la fecha y hora si no está vacía
            if datetime_str:
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            else:
                datetime_obj = None

            cursor.execute("INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (?, ?, ?, ?, ?)", 
                        (employee_id, name, datetime_obj, department_id, job_id))

# Función para cargar datos de trabajos
def load_jobs():
    with open('jobs.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            job_id = int(row[0])
            job_name = row[1]
            cursor.execute("INSERT INTO jobs (id, job) VALUES (?, ?)", (job_id, job_name))

# Función para cargar datos de departamentos
def load_departments():
    with open('departments.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            department_id = int(row[0])
            department_name = row[1]
            cursor.execute("INSERT INTO departments (id, department) VALUES (?, ?)", (department_id, department_name))

# Llamar a las funciones
load_hired_employees()
load_jobs()
load_departments()

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
