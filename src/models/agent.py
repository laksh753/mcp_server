from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class AgentBase(BaseModel):
    """Base agent model."""
    agent_id: str = Field(..., description="Unique identifier for the agent")
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional agent metadata")

class AgentCreate(AgentBase):
    """Model for creating a new agent."""
    pass

class AgentInDB(AgentBase):
    """Model for agent stored in database."""
    status: str = Field(default="registered", description="Current status of the agent")
    last_seen: datetime = Field(default_factory=datetime.utcnow, description="Last time agent was seen")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the agent was created")

class AgentUpdate(BaseModel):
    """Model for updating an agent."""
    status: Optional[str] = None
    capabilities: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None 