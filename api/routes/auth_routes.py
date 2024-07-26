from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.data_access.models import db, User, RoleEnum
from werkzeug.exceptions import Forbidden, Conflict, BadRequest

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        raise BadRequest('Missing fields')

    user = User.query.filter_by(username=username).first()
    if user:
        raise Conflict('User already exists')

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email, role=RoleEnum.JOB_SEEKER)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise BadRequest('Missing fields')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        raise Forbidden('Invalid credentials')

    access_token = create_access_token(identity={'id': user.id, 'role': str(user.role)})
    return jsonify(access_token=access_token), 200
