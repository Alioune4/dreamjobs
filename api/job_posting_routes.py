from flask import Blueprint, jsonify

job_posting_blueprint = Blueprint('job_posting_blueprint', __name__)

from api.models import JobPost, row_to_dict


@job_posting_blueprint.route('/', methods=['GET'])
def create_job():
    return jsonify([job_post.to_dict() for job_post in JobPost.query.all()])
