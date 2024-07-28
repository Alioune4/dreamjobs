import pytest
from api import create_app
from api.services.connection_service import db
from api.data_access.models import User, RoleEnum
from werkzeug.security import generate_password_hash
import json


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class='config.TestConfig')
    ctx = flask_app.app_context()
    ctx.push()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
        yield testing_client

    db.drop_all()
    ctx.pop()


@pytest.fixture(scope='module')
def init_database(test_client):
    return db


@pytest.fixture(scope='module')
def new_job_seeker(init_database):
    user = User(
        username='job_seeker',
        password=generate_password_hash('password'),
        email='job_seeker@example.com',
        role=RoleEnum.JOB_SEEKER
    )
    init_database.session.add(user)
    init_database.session.commit()
    return user


@pytest.fixture(scope='module')
def new_admin(init_database):
    user = User(
        username='admin',
        password=generate_password_hash('admin_password'),
        email='admin@example.com',
        role=RoleEnum.ADMIN
    )
    init_database.session.add(user)
    init_database.session.commit()
    return user


@pytest.fixture(scope='module')
def new_recruiter(init_database):
    user = User(
        username='recruiter',
        password=generate_password_hash('recruiter_password'),
        email='recruiter@example.com',
        role=RoleEnum.RECRUITER
    )
    init_database.session.add(user)
    init_database.session.commit()
    return user


@pytest.fixture
def login_as_admin(test_client, new_admin):
    response = test_client.post('/api/login', json={
        'username': new_admin.username,
        'password': 'admin_password'
    })
    data = json.loads(response.data)
    access_token = data.get('access_token')
    if access_token is None:
        print(f"Login response data for admin: {data}")  # Debugging line
        raise ValueError("No access token received")
    return access_token


@pytest.fixture
def login_as_recruiter(test_client, new_recruiter):
    response = test_client.post('/api/login', json={
        'username': new_recruiter.username,
        'password': 'recruiter_password'
    })
    data = json.loads(response.data)
    access_token = data.get('access_token')
    if access_token is None:
        print(f"Login response data for recruiter: {data}")
        raise ValueError("No access token received")
    return access_token


@pytest.fixture
def login_as_job_seeker(test_client, new_job_seeker):
    response = test_client.post('/api/login', json={
        'username': new_job_seeker.username,
        'password': 'password'
    })
    data = json.loads(response.data)
    access_token = data.get('access_token')
    if access_token is None:
        print(f"Login response data for job seeker: {data}")  # Debugging line
        raise ValueError("No access token received")
    return access_token


@pytest.fixture
def job_post_data():
    return {
        'title': 'Software Engineer',
        'description': 'We are looking for a software engineer',
        'location': 'Remote',
        'employment_type': 'Full-time',
        'category': 'Engineering',
        'salary': 100000
    }
