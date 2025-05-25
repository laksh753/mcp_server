from fastapi.testclient import TestClient
import pytest
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "running"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register_agent():
    agent_data = {
        "agent_id": "test_agent_1",
        "capabilities": ["test", "debug"],
        "metadata": {"version": "1.0.0"}
    }
    response = client.post("/agents/register", json=agent_data)
    assert response.status_code == 200
    assert response.json()["agent_id"] == "test_agent_1"

def test_get_agent():
    # First register an agent
    agent_data = {
        "agent_id": "test_agent_2",
        "capabilities": ["test"],
    }
    client.post("/agents/register", json=agent_data)
    
    # Then get the agent
    response = client.get("/agents/test_agent_2")
    assert response.status_code == 200
    assert response.json()["status"] == "registered"

def test_create_task():
    # First register an agent
    agent_data = {
        "agent_id": "test_agent_3",
        "capabilities": ["test"],
    }
    client.post("/agents/register", json=agent_data)
    
    # Then create a task
    task_data = {
        "agent_id": "test_agent_3",
        "type": "test_task",
        "parameters": {"test_param": "value"}
    }
    response = client.post("/tasks/create", json=task_data)
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_update_task_status():
    # First create a task
    agent_data = {
        "agent_id": "test_agent_4",
        "capabilities": ["test"],
    }
    client.post("/agents/register", json=agent_data)
    
    task_data = {
        "agent_id": "test_agent_4",
        "type": "test_task"
    }
    task_response = client.post("/tasks/create", json=task_data)
    task_id = task_response.json()["task_id"]
    
    # Then update its status
    status_data = {"status": "completed"}
    response = client.put(f"/tasks/{task_id}/status", json=status_data)
    assert response.status_code == 200
    
    # Verify the update
    task_response = client.get(f"/tasks/{task_id}")
    assert task_response.json()["status"] == "completed" 