from flask import Blueprint, request, jsonify

job_posting_blueprint = Blueprint('job_posting_blueprint', __name__)

from api.connection import db
from api.models import JobPost


@job_posting_blueprint.route('/jobs', methods=['GET'])
def create_job():
    return jsonify([job_post.to_dict() for job_post in JobPost.query.all()])
