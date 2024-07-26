from flask import Blueprint, jsonify, request
from api.services.connection_service import db
from api.services.data_validation_service import validate_job_post_data, validate_application_update_data, update_job_post
from api.data_access.models import JobPost, EmploymentTypeEnum, CategoryEnum
from api.services.auth_service import admin_or_recruiter_required


job_posting_blueprint = Blueprint('job_posting_blueprint', __name__)

@job_posting_blueprint.route('/', methods=['GET'])
def get_jobs():
    jobs = JobPost.query.all()
    return jsonify([job.to_dict() for job in jobs])


@job_posting_blueprint.route('/', methods=['POST'])
@admin_or_recruiter_required
def create_job():
    data = request.json

    errors = validate_job_post_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    job_post = JobPost(
        title=data['title'],
        description=data.get('description'),
        salary=data.get('salary'),
        location=data.get('location'),
        employment_type=EmploymentTypeEnum(data['employment_type']),
        category=CategoryEnum(data['category']),
    )
    db.session.add(job_post)
    db.session.commit()
    return jsonify(job_post.to_dict()), 201


@job_posting_blueprint.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job_post = JobPost.query.get(job_id)
    if job_post is None:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job_post.to_dict())


@job_posting_blueprint.route('/<int:job_id>', methods=['DELETE'])
@admin_or_recruiter_required
def delete_job(job_id):
    job_post = JobPost.query.get(job_id)
    if job_post is None:
        return jsonify({'error': 'Job not found'}), 404
    db.session.delete(job_post)
    db.session.commit()
    return jsonify({'message': 'Job deleted'}), 200


@job_posting_blueprint.route('/<int:job_id>', methods=['PUT'])
@admin_or_recruiter_required
def update_job(job_id):
    job_post = JobPost.query.get(job_id)
    if job_post is None:
        return jsonify({'error': 'Job not found'}), 404

    data = request.json

    errors = validate_application_update_data(data)

    if errors:
        return jsonify({'errors': errors}), 400

    update_job_post(job_post, data)

    db.session.commit()
    return jsonify(job_post.to_dict()), 200
