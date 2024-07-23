from flask import Flask

from config import Config
from flask_migrate import Migrate

from api.connection import db

def create_app():
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Initialize the migration
    migrate = Migrate(app, db)

    # Register the blueprints
    from .job_posting_routes import job_posting_blueprint
    app.register_blueprint(job_posting_blueprint)

    # import models so that they are detected by Alembic
    from api.models import User, JobPost

    return app
