import bcrypt

password = "nueva_contraseña"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
hashed_password = hashed.decode('utf-8')  # Convertir a string para guardar en SQLite.
