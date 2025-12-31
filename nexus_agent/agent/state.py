"""
State schemas for Nexus Agent
"""

from typing import Optional, Dict, Any
from langchain.agents import AgentState


class NexusAgentState(AgentState):
    """Extended state for Nexus Agent"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = {}
    conversation_stats: Dict[str, int] = {}
