import pytest

# 1. Test fetching tasks from an empty database
async def test_get_empty_tasks(client):
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert response.json() == []

# 2. Test unauthorized POST request (Missing X-API-Key)
async def test_create_task_unauthorized(client):
    payload = {"title": "Test Unauthorized Task", "completed": False}
    response = await client.post("/api/v1/tasks/", json=payload)
    assert response.status_code == 401

# 3. Test authorized POST request
async def test_create_task_success(client):
    headers = {"X-API-Key": "devflow-secret-key-2026"}
    payload = {"title": "Test Authorized Task", "completed": False}
    response = await client.post("/api/v1/tasks/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Authorized Task"
    assert "id" in data