from flask import Flask

from api.job_posting_routes import job_posting_blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Load the configuration
app.config.from_object(Config)
app.register_blueprint(job_posting_blueprint)

# Initialize extensions
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])