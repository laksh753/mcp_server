from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
import json
import os
from datetime import datetime


app = FastAPI(
    title="MCP Server",
    description="Management Control Protocol Server with dummy API endpoints",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


agents = {}
tasks = {}

# Helper functions
def get_agent_status(agent_id: str) -> Dict[str, Any]:
    """Get the current status of an agent."""
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents[agent_id]


@app.get("/")
async def root():
    """Root endpoint returning server status."""
    return {
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.post("/agents/register")
async def register_agent(agent_data: Dict[str, Any]):
    """Register a new agent with the MCP server."""
    agent_id = agent_data.get("agent_id")
    if not agent_id:
        raise HTTPException(status_code=400, detail="agent_id is required")
    
    agents[agent_id] = {
        "status": "registered",
        "capabilities": agent_data.get("capabilities", []),
        "last_seen": datetime.utcnow().isoformat(),
        "metadata": agent_data.get("metadata", {})
    }
    
    return {"status": "success", "agent_id": agent_id}

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent information."""
    return get_agent_status(agent_id)

@app.get("/agents")
async def list_agents():
    """List all registered agents."""
    return {
        "count": len(agents),
        "agents": agents
    }

@app.post("/tasks/create")
async def create_task(task_data: Dict[str, Any]):
    """Create a new task for an agent."""
    task_id = f"task_{len(tasks) + 1}"
    agent_id = task_data.get("agent_id")
    
    if not agent_id:
        raise HTTPException(status_code=400, detail="agent_id is required")
    
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    tasks[task_id] = {
        "task_id": task_id,
        "agent_id": agent_id,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "parameters": task_data.get("parameters", {}),
        "type": task_data.get("type", "unknown")
    }
    
    return {"status": "success", "task_id": task_id}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get task information."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.put("/tasks/{task_id}/status")
async def update_task_status(task_id: str, status_data: Dict[str, Any]):
    """Update task status."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks[task_id]["status"] = status_data.get("status", "unknown")
    tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
    
    return {"status": "success", "task_id": task_id}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_count": len(agents),
        "tasks_count": len(tasks)
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
