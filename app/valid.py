from utils import backup_database

result = backup_database()
if result:
    print("Respaldo realizado con éxito.")
else:
    print("Ocurrió un error durante el respaldo.")
