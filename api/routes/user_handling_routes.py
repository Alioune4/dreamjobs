from flask import Blueprint, jsonify, request
from api.services.connection_service import db
from api.data_access.models import User, RoleEnum
from api.services.auth_service import admin_required
from werkzeug.exceptions import NotFound
from api.services.data_validation_service import validate_user_data, get_enum_value_from_string

user_handling_blueprint = Blueprint('user_handling_blueprint', __name__)


@user_handling_blueprint.route('/', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@user_handling_blueprint.route('/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise NotFound('User not found')
    return jsonify(user.to_dict()), 200

@user_handling_blueprint.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise NotFound('User not found')
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

@user_handling_blueprint.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise NotFound('User not found')
    data = request.json
    validate_user_data(data, is_update=True)
    user.username = data['username']
    user.email = data['email']
    user.role = get_enum_value_from_string(RoleEnum, data['role'])
    db.session.commit()

    return jsonify(user.to_dict()), 200
