from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from api.services.connection_service import db


def create_app(config_class=Config):
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager()
    jwt.init_app(app)

    if not app.config['TESTING']:
        with app.app_context():
            # Create default admin user
            from .services.auth_service import create_default_admin_if_not_exists
            create_default_admin_if_not_exists()

    # Documentation
    from .routes.documentation_routes import swaggerui_blueprint, SWAGGER_URL
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)

    # Register the blueprints
    from .routes.auth_routes import auth_blueprint
    from .routes.job_posting_routes import job_posting_blueprint
    from .routes.application_routes import application_blueprint
    from .routes.user_handling_routes import user_handling_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/api')
    app.register_blueprint(job_posting_blueprint, url_prefix='/api/job-posts')
    app.register_blueprint(application_blueprint, url_prefix='/api/applications')
    app.register_blueprint(user_handling_blueprint, url_prefix='/api/users')

    # import models so that they are detected for migrations
    from api.data_access.models import User, JobPost, Application

    # Error handling
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({'error': e.description}), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        app.logger.exception(e)
        return jsonify({'error': 'Internal server error'}), 500

    return app
