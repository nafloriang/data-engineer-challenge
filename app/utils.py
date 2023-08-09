import os
import sqlite3
import shutil
import avro.schema
import json
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

DEFAULT_DB_PATH = "my_database.db"
BACKUP_PATH = "backup.db"
AVRO_BACKUP_DIR = "C:\\Users\\hopem\\Documents\\data-engineering-challenge\\backups"

TABLE_SCHEMAS = {
    "departments": {
        "fields": ["id", "department"],
        "schema": {
            "type": "record",
            "name": "departments",
            "fields": [
                {"name": "id", "type": ["int", "null"]},
                {"name": "department", "type": ["string", "null"]}
            ]
        }
    },
    "hired_employees": {
        "fields": ["id", "name", "datetime", "department_id", "job_id"],
        "schema": {
            "type": "record",
            "name": "hired_employees",
            "fields": [
                {"name": "id", "type": ["int", "null"]},
                {"name": "name", "type": ["string", "null"]},
                {"name": "datetime", "type": ["string", "null"]},
                {"name": "department_id", "type": ["int", "null"]},
                {"name": "job_id", "type": ["int", "null"]}
            ]
        }
    },
    "jobs": {
        "fields": ["id", "job"],
        "schema": {
            "type": "record",
            "name": "jobs",
            "fields": [
                {"name": "id", "type": ["int", "null"]},
                {"name": "job", "type": ["string", "null"]}
            ]
        }
    },
    "users": {
        "fields": ["id", "username", "password"],
        "schema": {
            "type": "record",
            "name": "users",
            "fields": [
                {"name": "id", "type": ["int", "null"]},
                {"name": "username", "type": ["string", "null"]},
                {"name": "password", "type": ["string", "null"]}
            ]
        }
    }
}

def backup_database(db_path=DEFAULT_DB_PATH):
    try:
        shutil.copy(db_path, BACKUP_PATH)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for table, data in TABLE_SCHEMAS.items():
                schema = avro.schema.parse(json.dumps(data["schema"]))
                rows = cursor.execute(f'SELECT * FROM {table}').fetchall()
                records = []

                for row in rows:
                    record = {field: row[idx] if not isinstance(row[idx], bytes) else row[idx].decode('utf-8') for idx, field in enumerate(data["fields"])}
                    records.append(record)

                avro_backup_path = os.path.join(AVRO_BACKUP_DIR, f'{table}_backup.avro')
                with open(avro_backup_path, 'wb') as file:
                    writer = DataFileWriter(file, DatumWriter(), schema)
                    for record in records:
                        writer.append(record)
                    writer.close()

        return True
    except Exception as e:
        print(f"Error al realizar backup: {e}")
        return False

def restore_database(backup_path=BACKUP_PATH, db_path=DEFAULT_DB_PATH):
    try:
        shutil.copy(backup_path, db_path)

        # Restauración desde los archivos AVRO
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for table, data in TABLE_SCHEMAS.items():
                avro_backup_path = os.path.join(AVRO_BACKUP_DIR, f'{table}_backup.avro')
                with open(avro_backup_path, 'rb') as file:
                    # Limpiar la tabla antes de restaurarla
                    cursor.execute(f'DELETE FROM {table}')

                    reader = DataFileReader(file, DatumReader())
                    for record in reader:
                        # Crear una sentencia INSERT
                        fields = ','.join(record.keys())
                        placeholders = ','.join('?' for _ in record.values())
                        cursor.execute(f'INSERT INTO {table} ({fields}) VALUES ({placeholders})', list(record.values()))
                    reader.close()

            conn.commit()

        return True
    except Exception as e:
        print(f"Error al restaurar: {e}")
        return False

# Si necesitas agregar más funciones o métodos, hazlo aquí.
