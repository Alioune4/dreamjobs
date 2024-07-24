from flask import Blueprint, jsonify

job_posting_blueprint = Blueprint('job_posting_blueprint', __name__)

from api.models import JobPost, row_to_dict


@job_posting_blueprint.route('/jobs', methods=['GET'])
def create_job():
    return jsonify([row_to_dict(job_post) for job_post in JobPost.query.all()])
