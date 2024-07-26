from flask import Flask, jsonify

from config import Config
from flask_migrate import Migrate

from api.services.connection_service import db

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
        from .services.auth_service import create_default_admin_if_not_exists
        create_default_admin_if_not_exists()

    # Register the blueprints
    from .routes.auth_routes import auth_blueprint
    from .routes.job_posting_routes import job_posting_blueprint
    from .routes.application_routes import application_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/api')
    app.register_blueprint(job_posting_blueprint, url_prefix='/api/job-posts')
    app.register_blueprint(application_blueprint, url_prefix='/api/applications')

    # import models so that they are detected for migrations
    from api.data_access.models import User, JobPost, Application

    # Error handling
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({'error': e.description}), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app
