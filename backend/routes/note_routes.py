from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from extensions import db, socketio, cache
from models import Note, User
from utils.conflict_resolver import resolve_conflicts
from flask_caching import Cache

note_routes = Blueprint('note_routes', __name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})

@note_routes.route('/notes', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def get_notes():
    user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=user_id).all()
    return jsonify([note.to_dict() for note in notes]), 200

@note_routes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    note = Note(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@note_routes.route('/notes/<int:id>', methods=['PUT'])
@jwt_required()
def update_note_endpoint(id):
    user_id = get_jwt_identity()
    data = request.json
    existing_note = Note.query.filter_by(id=id, user_id=user_id).first_or_404()
    updated_note = resolve_conflicts(existing_note, data)
    existing_note.title = updated_note['title']
    existing_note.content = updated_note['content']
    db.session.commit()
    socketio.emit('note_updated', {"id": existing_note.id, "title": existing_note.title, "content": existing_note.content}, broadcast=True)
    return jsonify({"id": existing_note.id, "title": existing_note.title, "content": existing_note.content}), 200

@note_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@note_routes.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note_endpoint(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted successfully'}), 200
    return jsonify({'message': 'Note not found'}), 404
