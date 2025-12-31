"""
Nexus Agent Package
Modular agent implementation using LangChain
"""

# State
from .state import NexusAgentState

# Tools
from .tools import (
    lookup_company_policy,
    get_contact_info,
    search_knowledge_base,
    get_onboarding_guide,
    NEXUS_TOOLS
)

# Middleware
from .middleware import (
    SafetyMiddleware,
    NexusModelSelectionMiddleware,
    NexusPromptMiddleware,
    ToolErrorMiddleware
)

# Prompts
from .prompts import (
    BASE_SYSTEM_PROMPT,
    get_system_prompt
)

# Main Agent
from .agent import (
    AgentResponse,
    NexusLangChainAgent,
    create_nexus_agent
)

# Backward compatibility - re-export from original langchain_agent.py
from .agent import NexusLangChainAgent as LangChainAgent

__all__ = [
    # State
    "NexusAgentState",
    
    # Tools
    "lookup_company_policy",
    "get_contact_info",
    "search_knowledge_base",
    "get_onboarding_guide",
    "NEXUS_TOOLS",
    
    # Middleware
    "SafetyMiddleware",
    "NexusModelSelectionMiddleware",
    "NexusPromptMiddleware",
    "ToolErrorMiddleware",
    
    # Prompts
    "BASE_SYSTEM_PROMPT",
    "get_system_prompt",
    
    # Main Agent
    "AgentResponse",
    "NexusLangChainAgent",
    "create_nexus_agent",
    "LangChainAgent",  # Backward compatibility
]
