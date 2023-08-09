# utils.py
import sqlite3
import shutil

def backup_database():
    try:
        # Ruta de la base de datos SQLite
        db_path = 'C:/Users/hopem/Documents/data-engineering-challenge/mydatabase.db'
        
        # Copiar la base de datos a un archivo de respaldo
        shutil.copy(db_path, 'backup.db')
        
        return True
    except Exception as e:
        print(e)
        return False

def restore_database():
    try:
        # Rutas de las bases de datos
        backup_path = 'backup.db'
        db_path = 'C:/Users/hopem/Documents/data-engineering-challenge/mydatabase.db'
        
        # Restaurar la base de datos desde el archivo de respaldo
        shutil.copy(backup_path, db_path)
        
        return True
    except Exception as e:
        print(e)
        return False