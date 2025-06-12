import pytest
from datetime import date
from app.models import user_model

def test_signup(client, db_session):
    payload = {
        "name": "Test User",
        "username": "test@example.com",
        "password": "testpassword",
        "dob": str(date(1990, 1, 1)),
        "gender": "female"
    }

    response = client.post('/signup', json=payload)

    assert response.status_code == 201
    user = db_session.query(user_model.User).filter_by(username="test@example.com").first()
    assert user is not None
    assert user.name == "Test User"
 

def test_login(client, db_session):
    payload = {
        "name": "Test User",
        "username": "test@example.com",
        "password": "testpassword",
        "dob": str(date(1990, 1, 1)),
        "gender": "female"
    }

    client.post('/signup', json=payload)

    payload  = {
        "username": "test@example.com",
        "password": "testpassword",
    }

    user = db_session.query(user_model.User).filter_by(username="test@example.com").first()
    user.is_verified = True

    response = client.post('/login', data=payload)
    assert response.status_code == 200