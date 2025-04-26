import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_notification(client):
    response = client.post('/notifications', json={
        "content": "Test1 notification",
        "priority": "high"
    })
    print(response.json)  # Debugging: Print the response JSON
    assert response.status_code == 200
    assert response.json["message"] == "Notification added successfully!"

def test_get_notifications(client):
    response = client.get('/notifications')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_notification(client):
    # Add a notification first
    client.post('/notifications', json={
        "content": "Test notification",
        "priority": "high"
    })
    # Update the notification
    response = client.put('/notifications/1', json={
        "content": "Updated notification",
        "priority": "low"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Notification updated successfully!"

def test_delete_notification(client):
    # Add a notification first
    client.post('/notifications', json={
        "content": "Test notification",
        "priority": "high"
    })
    # Delete the notification
    response = client.delete('/notifications/1')
    assert response.status_code == 200
    assert response.json["message"] == "Notification deleted successfully!"

def test_prioritize(client):
    response = client.post('/prioritize', json={
        "content": "Urgent meeting with the team at 3 PM"
    })
    print(response.json)  # Debugging: Print the response JSON
    assert response.status_code == 200
    assert response.json["priority"] in ["high", "medium", "low"]