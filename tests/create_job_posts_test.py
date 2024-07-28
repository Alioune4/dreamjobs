import json
from werkzeug import exceptions


def assert_job_post_response(response, job_post, ignore_location=False, ignore_salary=False):
    assert response.status_code == 201
    job_post_response = json.loads(response.data)

    assert job_post_response['title'] == job_post['title']
    assert job_post_response['description'] == job_post['description']
    assert job_post_response['employment_type'] == job_post['employment_type']
    assert job_post_response['category'] == job_post['category']
    assert ignore_location or job_post_response['location'] == job_post['location']
    assert ignore_salary or job_post_response['salary'] == job_post['salary']


def test_create_job_post_admin(test_client, login_as_admin, job_post_data):
    response = test_client.post('/api/job-posts/', json=job_post_data,
                                headers={'Authorization': f'Bearer {login_as_admin}'})
    assert_job_post_response(response, job_post_data)


def test_create_job_post_recruiter(test_client, login_as_recruiter, job_post_data):
    response = test_client.post('/api/job-posts/', json=job_post_data,
                                headers={'Authorization': f'Bearer {login_as_recruiter}'})
    assert_job_post_response(response, job_post_data)


def test_create_job_post_not_authenticated(test_client, job_post_data):
    response = test_client.post('/api/job-posts/', json=job_post_data)
    assert response.status_code == exceptions.Unauthorized.code


def test_create_job_post_job_seeker(test_client, login_as_job_seeker, job_post_data):
    response = test_client.post('/api/job-posts/', json=job_post_data,
                                headers={'Authorization': f'Bearer {login_as_job_seeker}'})
    assert response.status_code == exceptions.Forbidden.code


def test_create_job_post_missing_not_mandatory_fields(test_client, login_as_admin, job_post_data):
    job_post_data_no_salary = job_post_data.copy()
    job_post_data_no_salary.pop('salary')  # salary is not required
    response = test_client.post('/api/job-posts/', json=job_post_data_no_salary,
                                headers={'Authorization': f'Bearer {login_as_admin}'})
    assert_job_post_response(response, job_post_data_no_salary, ignore_salary=True)


def test_create_job_post_missing_mandatory_fields(test_client, login_as_admin, job_post_data):
    job_post_without_title = job_post_data.copy()
    job_post_without_title.pop('title')
    response = test_client.post('/api/job-posts/', json=job_post_without_title,
                                headers={'Authorization': f'Bearer {login_as_admin}'})
    assert response.status_code == exceptions.BadRequest.code


def test_create_job_post_invalid_category(test_client, login_as_admin, job_post_data):
    job_post_invalid_category = job_post_data.copy()
    job_post_invalid_category['category'] = 'Invalid'
    response = test_client.post('/api/job-posts/', json=job_post_invalid_category,
                                headers={'Authorization': f'Bearer {login_as_admin}'})
    assert response.status_code == exceptions.BadRequest.code


def test_create_job_post_invalid_employment_type(test_client, login_as_admin, job_post_data):
    job_post_invalid_employment_type = job_post_data.copy()
    job_post_invalid_employment_type['employment_type'] = 'Invalid'
    response = test_client.post('/api/job-posts/', json=job_post_invalid_employment_type,
                                headers={'Authorization': f'Bearer {login_as_admin}'})
    assert response.status_code == exceptions.BadRequest.code