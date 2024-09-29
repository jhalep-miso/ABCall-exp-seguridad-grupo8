from flask import Blueprint, request, jsonify
from .models import db, User
from .utils import generate_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario registrado de manera exitosa"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_jwt(user.id)
        return jsonify({"token": token, "user": user.to_dict()}), 200
    return jsonify({"message": "Credenciales invalidas"}), 401

