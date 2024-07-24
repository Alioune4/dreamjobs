from flask import Flask

from config import Config
from flask_migrate import Migrate

from api.connection import db

def create_app():
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object(Config)

    # Connect sqlalchemy to the app
    db.init_app(app)

    # Initialize the migration
    migrate = Migrate(app, db)

    # Register the blueprints
    from .job_posting_routes import job_posting_blueprint
    from .job_categories_routes import category_blueprint
    app.register_blueprint(job_posting_blueprint, url_prefix='/api/job-posts')
    app.register_blueprint(category_blueprint, url_prefix='/api/categories')

    # import models so that they are detected for migrations
    from api.models import User, JobPost

    return app
