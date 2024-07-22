from flask import Blueprint

job_posting_blueprint = Blueprint('job_posting_blueprint', __name__)


@job_posting_blueprint.route('/jobs', methods=['GET'])
def create_job():
    return "To implement"