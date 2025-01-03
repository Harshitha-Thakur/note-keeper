import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_notes(client):
    response = client.get('/api/notes')
    assert response.status_code == 200

def test_add_note(client):
    response = client.post('/api/notes', json={"title": "Test Note", "content": "Test Content"})
    assert response.status_code == 201
