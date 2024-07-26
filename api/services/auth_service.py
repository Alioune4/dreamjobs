from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from werkzeug.security import generate_password_hash

from api.data_access.models import User, RoleEnum
from flask import jsonify
from api.services.connection_service import db


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user['id']).first()
        if user.role != RoleEnum.ADMIN:
            return jsonify({"msg": "Admins only!"}), 403
        return fn(*args, **kwargs)

    return wrapper

def admin_or_recruiter_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user['id']).first()
        if user.role != RoleEnum.ADMIN and user.role != RoleEnum.RECRUITER:
            return jsonify({"msg": "Admins and recruiters only!"}), 403
        return fn(*args, **kwargs)

    return wrapper


def create_default_admin_if_not_exists():
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_password = generate_password_hash('adminpassword')
        admin_user = User(username='admin', password=hashed_password, email='admin@example.com', role=RoleEnum.ADMIN)
        db.session.add(admin_user)
        db.session.commit()
