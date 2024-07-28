import json
import pytest

def test_get_all_job_posts(test_client):
    response = test_client.get('/api/job-posts/')
    assert response.status_code == 200

def test_create_job_post(test_client, login_as_admin):
    response = test_client.post('/api/job-posts/', json={
        'title': 'Software Engineer',
        'description': 'We are looking for a software engineer',
        'location': 'Remote',
        'employment_type': 'Full-time',
        'category': 'Engineering'
    }, headers={'Authorization': f'Bearer {login_as_admin}'})
    assert response.status_code == 201

def test_create_job_post_missing_fields(test_client, login_as_admin):
    response = test_client.post('/api/job-posts/', json={
        'title': 'Software Engineer',
        'description': 'We are looking for a software engineer',
        'location': 'Remote',
        'employment_type': 'Full-time',
    }, headers={'Authorization': f'Bearer {login_as_admin}'})
    assert response.status_code == 400
    assert 'error' in json.loads(response.data)

def test_create_job_post_invalid_fields(test_client, login_as_admin):
    response = test_client.post('/api/job-posts/', json={
        'title': 'Software Engineer',
        'description': 'We are looking for a software engineer',
        'location': 'Remote',
        'employment_type': 'Full-time',
        'category': 'Invalid'
    }, headers={'Authorization': f'Bearer {login_as_admin}'})
    assert response.status_code == 400
    assert 'error' in json.loads(response.data)

def test_create_job_post_unauthorized(test_client):
    response = test_client.post('/api/job-posts/', json={
        'title': 'Software Engineer',
        'description': 'We are looking for a software engineer',
        'location': 'Remote',
        'employment_type': 'Full-time',
        'category': 'Engineering'
    })
    assert response.status_code == 401

def test_create_job_post_job_seeker(test_client, login_as_job_seeker):
    response = test_client.post('/api/job-posts/', json={
        'title': 'Software Engineer',
        'description': 'We are looking for a software engineer',
        'location': 'Remote',
        'employment_type': 'Full-time',
        'category': 'Engineering'
    }, headers={'Authorization': f'Bearer {login_as_job_seeker}'})
    assert response.status_code == 403