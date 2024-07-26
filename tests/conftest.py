import pytest
from api import create_app
from api.services.connection_service import db
from config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    app = create_app(config_class=TestConfig)

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client

    with app.app_context():
        db.drop_all()
    return app

@pytest.fixture(scope='module')
def test_db():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()