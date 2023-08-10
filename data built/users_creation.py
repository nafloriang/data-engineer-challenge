import bcrypt
import sqlite3

DATABASE = 'mydatabase.db'

def set_password(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
    
    conn.commit()
    conn.close()
    
    print("Password updated successfully!")

if __name__ == "__main__":
    set_password("admin", "1016082760")
