from flask import Flask

from config import Config
from flask_migrate import Migrate

from api.connection import db

from flask_jwt_extended import JWTManager

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    with app.app_context():
        # Create default admin user
        from .auth_service import create_default_admin
        create_default_admin()

    # Register the blueprints
    from .job_posting_routes import job_posting_blueprint
    from .auth_routes import auth_blueprint

    app.register_blueprint(job_posting_blueprint, url_prefix='/api/job-posts')
    app.register_blueprint(auth_blueprint, url_prefix='/api')

    # import models so that they are detected for migrations
    from api.models import User, JobPost

    return app
