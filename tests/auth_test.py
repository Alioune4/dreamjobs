import json
import pytest

def test_register(test_client):
    response = test_client.post('/api/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 201


def test_register_login(test_client):
    test_client.post('/api/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com'
    })

    response = test_client.post('/api/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data)