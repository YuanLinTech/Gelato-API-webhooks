# init_consumer.py
from flask import Flask

# Create a Flask instance
app = Flask(__name__)

# Load Flask configurations from config.py
app.secret_key = app.config['SECRET_KEY']
app.config.from_object("config")

# Setup the Flask SocketIO integration
from flask_socketio import SocketIO
socketio = SocketIO(app,logger=True,engineio_logger=True)
