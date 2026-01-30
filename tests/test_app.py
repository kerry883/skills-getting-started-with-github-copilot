import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    # Use a unique email to avoid duplicate error
    response = client.post("/activities/Art Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Art Club" in response.json()["message"]

    # Try signing up again (should fail)
    response = client.post("/activities/Art Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

def test_unregister_participant():
    # First, sign up a user
    client.post("/activities/Drama Society/signup", params={"email": "removeuser@mergington.edu"})
    # Now, remove them
    response = client.delete("/activities/Drama Society/unregister", params={"email": "removeuser@mergington.edu"})
    assert response.status_code == 200
    assert "Removed removeuser@mergington.edu from Drama Society" in response.json()["message"]
    # Try removing again (should fail)
    response = client.delete("/activities/Drama Society/unregister", params={"email": "removeuser@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
