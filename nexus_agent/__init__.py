"""
Nexus Agent - 新员工入职助手
"""

__version__ = "0.1.0"
__author__ = "Nexus Team"

# Import the new LangChain-based agent
try:
    from .agent import (
        NexusLangChainAgent,
        create_nexus_agent,
        AgentResponse,
        NexusAgentState
    )
    _langchain_agent_available = True
except ImportError:
    _langchain_agent_available = False
    NexusLangChainAgent = None
    create_nexus_agent = None
    AgentResponse = None
    NexusAgentState = None

# Import legacy agent for backward compatibility (optional)
try:
    from .agent.core import NexusAgent
    _legacy_available = True
except ImportError:
    _legacy_available = False
    NexusAgent = None

# Import RAG components
try:
    from .rag import (
        NexusDocumentLoader,
        NexusTextSplitter,
        NexusEmbeddings,
        NexusVectorStore,
        NexusIndexingPipeline,
        NexusRetriever,
    )
    _rag_available = True
except ImportError:
    _rag_available = False
    NexusDocumentLoader = None
    NexusTextSplitter = None
    NexusEmbeddings = None
    NexusVectorStore = None
    NexusIndexingPipeline = None
    NexusRetriever = None

# Import RAG Agent
try:
    from .agent.rag_agent import (
        NexusRAGAgent,
        NexusRAGAgentWithMemory,
    )
    _rag_agent_available = True
except ImportError:
    _rag_agent_available = False
    NexusRAGAgent = None
    NexusRAGAgentWithMemory = None

__all__ = [
    # LangChain Agent
    "NexusLangChainAgent",
    "create_nexus_agent",
    "AgentResponse",
    "NexusAgentState",
    # Legacy Agent
    "NexusAgent",
    # RAG Components
    "NexusDocumentLoader",
    "NexusTextSplitter",
    "NexusEmbeddings",
    "NexusVectorStore",
    "NexusIndexingPipeline",
    "NexusRetriever",
    # RAG Agent
    "NexusRAGAgent",
    "NexusRAGAgentWithMemory",
]