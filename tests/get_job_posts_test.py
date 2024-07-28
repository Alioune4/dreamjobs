import json

def test_get_all_job_posts(test_client):
    response = test_client.get('/api/job-posts/')
    assert response.status_code == 200

def test_get_job_post_admin(test_client, login_as_admin):
    response = test_client.get('/api/job-posts/', headers = {'Authorization': f'Bearer {login_as_admin}'})
    assert response.status_code == 200

def test_get_job_post_recruiter(test_client, login_as_recruiter):
    response = test_client.get('/api/job-posts/', headers = {'Authorization': f'Bearer {login_as_recruiter}'})
    assert response.status_code == 200

def test_get_job_post_job_seeker(test_client, login_as_job_seeker):
    response = test_client.get('/api/job-posts/', headers = {'Authorization': f'Bearer {login_as_job_seeker}'})
    assert response.status_code == 200