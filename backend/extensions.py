from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
socketio = SocketIO()
cache = Cache()
jwt = JWTManager()