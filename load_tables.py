import sqlite3
import csv
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('mydatabase.db')  # Cambia 'mydatabase.db' al nombre de tu archivo de base de datos
cursor = conn.cursor()

# Leer el archivo CSV y insertar datos en la tabla
with open('hired_employees.csv', 'r') as csv_file:  # Cambia 'hired_employees.csv' al nombre de tu archivo CSV
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

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
