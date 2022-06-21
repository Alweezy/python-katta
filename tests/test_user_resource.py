from fastapi import status, testclient

from untapped.api.resources import app

client = testclient.TestClient(app)


def test_create_user_happy_path():
    response = client.post(
        "/users",
        headers={"ContentType": "application/json"},
        json={
            "first_name": "daniel",
            "email": "test1@email.com",
            "password": "pass"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["first_name"] == "daniel"
    assert response.json()["email"] == "test1@email.com"


def test_create_user_fails_on_duplicate_email():
    response = client.post(
        "/users",
        headers={"ContentType": "application/json"},
        json={
            "first_name": "daniel",
            "email": "test2@email.com",
            "password": "pass"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "test2@email.com"

    # attempt duplicate email
    response2 = client.post(
        "/users",
        headers={"ContentType": "application/json"},
        json={
            "first_name": "daniel",
            "email": "test2@email.com",
            "password": "pass"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_409_CONFLICT
    assert response2.json()["detail"] == "A user with that email already exists"


def test_create_user_fails_on_invalid_email_format():
    response = client.post(
        "/users",
        headers={"ContentType": "application/json"},
        json={
            "first_name": "daniel",
            "email": "randomString",
            "password": "pass"
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "The email address is not valid. It must have exactly one @-sign."
