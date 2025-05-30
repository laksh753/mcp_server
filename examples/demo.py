import requests
import time
import json

def print_response(response):
    """Pretty print API response."""
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def main():
    base_url = "http://localhost:8000"
    
   
    print("\n1. Checking server health...")
    response = requests.get(f"{base_url}/health")
    print_response(response)
    
    
    print("\n2. Registering a new agent...")
    agent_data = {
        "agent_id": "demo_agent_1",
        "capabilities": ["test", "echo", "compute"],
        "metadata": {
            "version": "1.0.0",
            "environment": "demo"
        }
    }
    response = requests.post(f"{base_url}/agents/register", json=agent_data)
    print_response(response)
    
    
    print("\n3. Getting agent information...")
    response = requests.get(f"{base_url}/agents/demo_agent_1")
    print_response(response)
    
   
    print("\n4. Creating a task...")
    task_data = {
        "agent_id": "demo_agent_1",
        "type": "echo",
        "parameters": {
            "message": "Hello, MCP!",
            "priority": "high"
        }
    }
    response = requests.post(f"{base_url}/tasks/create", json=task_data)
    print_response(response)
    task_id = response.json()["task_id"]
    
   
    print("\n5. Getting task status...")
    response = requests.get(f"{base_url}/tasks/{task_id}")
    print_response(response)
    
    
    print("\n6. Updating task status...")
    status_data = {"status": "completed"}
    response = requests.put(f"{base_url}/tasks/{task_id}/status", json=status_data)
    print_response(response)
    
   
    print("\n7. Listing all agents...")
    response = requests.get(f"{base_url}/agents")
    print_response(response)

if __name__ == "__main__":
    main() 
