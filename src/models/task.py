from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class TaskBase(BaseModel):
    """Base task model."""
    agent_id: str = Field(..., description="ID of the agent to execute the task")
    type: str = Field(..., description="Type of task to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")

class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass

class TaskInDB(TaskBase):
    """Model for task stored in database."""
    task_id: str = Field(..., description="Unique identifier for the task")
    status: str = Field(default="pending", description="Current status of the task")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the task was created")
    updated_at: Optional[datetime] = Field(None, description="Last time task was updated")
    completed_at: Optional[datetime] = Field(None, description="When the task was completed")
    result: Optional[Dict[str, Any]] = Field(None, description="Task execution result")

class TaskUpdate(BaseModel):
    """Model for updating a task."""
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None 