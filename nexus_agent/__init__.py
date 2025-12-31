"""
Nexus Agent - 新员工入职助手
"""

__version__ = "0.1.0"
__author__ = "Nexus Team"

# Import the new LangChain-based agent
from .agent.langchain_agent import (
    NexusLangChainAgent,
    create_nexus_agent,
    AgentResponse,
    NexusAgentState
)

# Import legacy agent for backward compatibility (optional)
try:
    from .agent.core import NexusAgent
    _legacy_available = True
except ImportError:
    _legacy_available = False
    NexusAgent = None

__all__ = [
    "NexusLangChainAgent",
    "create_nexus_agent",
    "AgentResponse",
    "NexusAgentState",
    "NexusAgent",  # Legacy (may be None if dependencies missing)
]