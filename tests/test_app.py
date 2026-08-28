from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email():
    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")
    assert response.status_code == 200

    response = client.delete("/activities/Chess Club/participants?email=teststudent@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered teststudent@mergington.edu from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert "teststudent@mergington.edu" not in activity["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
