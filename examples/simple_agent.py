import requests
import time
import uuid
from datetime import datetime

class SimpleAgent:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url
        self.agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        self.capabilities = ["basic_task", "echo"]
        self.registered = False

    def register(self):
        """Register the agent with the MCP server."""
        data = {
            "agent_id": self.agent_id,
            "capabilities": self.capabilities,
            "metadata": {
                "version": "1.0.0",
                "type": "simple_agent",
                "started_at": datetime.utcnow().isoformat()
            }
        }
        
        response = requests.post(f"{self.server_url}/agents/register", json=data)
        if response.status_code == 200:
            self.registered = True
            print(f"Agent {self.agent_id} registered successfully")
            return True
        else:
            print(f"Failed to register agent: {response.text}")
            return False

    def check_tasks(self):
        """Check for any pending tasks."""
        response = requests.get(f"{self.server_url}/agents/{self.agent_id}")
        if response.status_code == 200:
            return response.json()
        return None

    def execute_task(self, task_id, task_type, parameters):
        """Execute a task and update its status."""
        print(f"Executing task {task_id} of type {task_type}")
        
        
        time.sleep(2)
        
        
        status_data = {"status": "completed"}
        response = requests.put(
            f"{self.server_url}/tasks/{task_id}/status",
            json=status_data
        )
        
        if response.status_code == 200:
            print(f"Task {task_id} completed successfully")
            return True
        else:
            print(f"Failed to update task status: {response.text}")
            return False

    def run(self):
        """Main agent loop."""
        if not self.registered and not self.register():
            return
        
        print(f"Agent {self.agent_id} starting main loop...")
        
        try:
            while True:
                
                agent_status = self.check_tasks()
                if agent_status:
                    print(f"Agent status: {agent_status}")
                
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\nAgent shutting down...")

if __name__ == "__main__":
    agent = SimpleAgent()
    agent.run() 
