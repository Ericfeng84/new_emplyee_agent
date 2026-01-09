from functools import lru_cache
from nexus_agent.agent.agent import create_nexus_agent, NexusLangChainAgent

@lru_cache()
def get_nexus_agent() -> NexusLangChainAgent:
    """
    Get or create a NexusLangChainAgent instance.
    Uses lru_cache to ensure singleton pattern per worker.
    """
    # Assuming default configuration is sufficient
    return create_nexus_agent(enable_memory=True)
