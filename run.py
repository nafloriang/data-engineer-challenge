# run.py

# Notify that the application is starting
print("Starting the application...")

# Import the Flask app instance from the 'app' module
from app import app

# Check if this script is being run as the main module, 
# and if so, start the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
