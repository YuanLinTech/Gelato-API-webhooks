# init_producer.py
from flask import Flask

# Create a Flask instance
# The value of __name__ is "__main__" when the program is run directly by the Python interpreter.
# while when the module is imported, the value of __name__ equals the name of the file to which the module is imported
# app will be initialised as Flask(file_name), where file_name is the name of the file to which the init_produced is imported
app = Flask(__name__)

# Load Flask configurations from config.py
app.secret_key = app.config['SECRET_KEY']
app.config.from_object("config")
