from flask import Blueprint, jsonify, request
from api.services.connection_service import db
from api.data_access.models import Application, RoleEnum, JobPost, ApplicationStatusEnum, User
from api.services.data_validation_service import validate_application_data, validate_application_update_data
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

application_blueprint = Blueprint('application_blueprint', __name__)


@application_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_applications():
    user = get_jwt_identity()
    if user['role'] == RoleEnum.ADMIN.value or user['role'] == RoleEnum.RECRUITER.value:
        applications = Application.query.all()
    else:
        applications = Application.query.filter_by(user_id=user['id']).all()
    return jsonify([application.to_dict() for application in applications])


@application_blueprint.route('/<int:application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    application = Application.query.get(application_id)

    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if user.role != RoleEnum.ADMIN.value and user.role != RoleEnum.RECRUITER and user.id != application.user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    if not application:
        return jsonify({'message': 'Application not found'}), 404
    return jsonify(application.to_dict())


@application_blueprint.route('/', methods=['POST'])
@jwt_required()
def apply():
    data = request.get_json()

    errors = validate_application_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    job_post = JobPost.query.get(data['job_post_id'])
    if not job_post:
        return jsonify({'message': 'Job post not found'}), 404

    application = Application(
        user_id=user.id,
        job_post_id=job_post.id,
        resume=data['resume'],
        cover_letter=data.get('cover_letter', None),
        status=ApplicationStatusEnum.PENDING
    )
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'}), 201


@application_blueprint.route('/<int:application_id>', methods=['PUT'])
@jwt_required()
def update_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'message': 'Application not found'}), 404

    data = request.get_json()

    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if user.role != RoleEnum.ADMIN.value and user.id != application.user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    errors = validate_application_update_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    for key, value in data.items():
        setattr(application, key, value)

    db.session.commit()
    return jsonify({'message': 'Application updated successfully'}), 200


@application_blueprint.route('/<int:application_id>', methods=['DELETE'])
@jwt_required()
def delete_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'message': 'Application not found'}), 404

    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if user.role != RoleEnum.ADMIN.value and user.id != application.user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(application)
    db.session.commit()
    return jsonify({'message': 'Application deleted successfully'}), 200
