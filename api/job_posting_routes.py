from flask import Blueprint, jsonify, request
from api.connection import db
from api.data_validation import validate_job_post_data, validate_update_data
from api.models import JobPost, EmploymentTypeEnum, CategoryEnum


job_posting_blueprint = Blueprint('job_posting_blueprint', __name__)

@job_posting_blueprint.route('/', methods=['GET'])
def get_jobs():
    jobs = JobPost.query.all()
    return jsonify([job.to_dict() for job in jobs])


@job_posting_blueprint.route('/', methods=['POST'])
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
def delete_job(job_id):
    job_post = JobPost.query.get(job_id)
    if job_post is None:
        return jsonify({'error': 'Job not found'}), 404
    db.session.delete(job_post)
    db.session.commit()
    return jsonify({'message': 'Job deleted'}), 200


@job_posting_blueprint.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job_post = JobPost.query.get(job_id)
    if job_post is None:
        return jsonify({'error': 'Job not found'}), 404

    data = request.json

    errors = validate_update_data(data)

    if errors:
        return jsonify({'errors': errors}), 400

    for key, value in data.items():
        if hasattr(job_post, key):
            setattr(job_post, key, value)

    db.session.commit()
    return jsonify(job_post.to_dict()), 200
