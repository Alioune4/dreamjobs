from flask import Flask

app = Flask(__name__)

from api.job_posting_routes import job_posting_blueprint
app.register_blueprint(job_posting_blueprint)