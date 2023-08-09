from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# JWT Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

# Initialize JWT Manager
jwt = JWTManager(app)

# Registrar el Blueprint
from .routes import routes
app.register_blueprint(routes)
