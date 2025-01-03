from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from config import Config
from models import db, User
from flask_jwt_extended import JWTManager, create_access_token
from routes.note_routes import note_routes
from routes.auth_routes import auth_bp
from extensions import socketio, cache
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

try:
    db.init_app(app)
except Exception as e:
    app.logger.error(f"Database initialization failed: {e}")
    raise

try:
    jwt = JWTManager(app)
except Exception as e:
    app.logger.error(f"JWT setup failed: {e}")
    raise

socketio.init_app(app)
cache.init_app(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    response = {
        "message": str(e),
        "type": e.__class__.__name__
    }
    return jsonify(response), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204

# Serve static files
@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('static', path)

app.register_blueprint(note_routes, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.error(f"Database creation failed: {e}")
        raise

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Add your registration logic here
    return jsonify({'message': 'Registration successful'}), 201

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    response = {
        "message": str(e),
        "type": e.__class__.__name__
    }
    return jsonify(response), 500

if __name__ == '__main__':
    # Set up logging to a file
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    
    app.run(debug=True, host='0.0.0.0', port=5000)