from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Puedes cambiar esto a otro sistema de base de datos SQL si lo prefieres
db = SQLAlchemy(app)
