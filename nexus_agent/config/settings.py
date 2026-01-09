"""
Nexus Agent Configuration Management
"""

from pydantic_settings import BaseSettings
from typing import Optional, Literal
from pydantic import Field


class NexusConfig(BaseSettings):
    """Nexus Agent Configuration"""
    
    # LLM Configuration
    llm_provider: Literal["openai", "deepseek", "qwen"] = Field(
        default="openai", 
        description="LLM provider to use"
    )
    llm_model: str = Field(
        default="gpt-4o",
        description="LLM model name"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="LLM temperature for response randomness"
    )
    
    # API Keys
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key"
    )
    deepseek_api_key: Optional[str] = Field(
        default=None,
        description="DeepSeek API key"
    )
    qwen_api_key: Optional[str] = Field(
        default=None,
        description="Qwen API key"
    )
    
    # Logging Configuration
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level"
    )
    log_file: Optional[str] = Field(
        default=None,
        description="Log file path (if not specified, logs to console)"
    )
    
    # Safety Configuration
    max_conversation_length: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of conversation messages to keep in context"
    )
    enable_safety_checks: bool = Field(
        default=True,
        description="Enable input/output safety validation"
    )
    
    # Performance Configuration
    max_retries: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of retries for LLM calls"
    )
    retry_delay: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="Base delay between retries (in seconds)"
    )
    
    # Token Management
    max_tokens: int = Field(
        default=1000,
        ge=100,
        le=8000,
        description="Maximum tokens for conversation context"
    )
    
    # Sprint 2: RAG Configuration
    # Document Loading
    data_directory: str = Field(
        default="nexus_agent/data/documents",
        description="Directory containing documents for RAG"
    )
    
    # Text Splitting
    chunk_size: int = Field(
        default=1000,
        ge=100,
        le=4000,
        description="Maximum chunk size for document splitting"
    )
    chunk_overlap: int = Field(
        default=200,
        ge=0,
        le=1000,
        description="Overlap between chunks"
    )
    text_splitter_strategy: Literal["recursive", "markdown"] = Field(
        default="recursive",
        description="Text splitting strategy"
    )
    
    # Embeddings (BGE - 优化中文理解)
    embedding_model: str = Field(
        default="BAAI/bge-small-zh-v1.5",
        description="Embedding model name (optimized for Chinese)"
    )
    embedding_device: Literal["cpu", "cuda"] = Field(
        default="cpu",
        description="Device for embedding generation"
    )
    normalize_embeddings: bool = Field(
        default=True,
        description="Whether to normalize embeddings (important for BGE models)"
    )
    
    # Vector Store (Chroma)
    vector_store_type: Literal["chroma"] = Field(
        default="chroma",
        description="Type of vector store"
    )
    chroma_collection: str = Field(
        default="nexus_knowledge_base",
        description="Chroma collection name"
    )
    chroma_persist_dir: Optional[str] = Field(
        default="nexus_agent/data/chroma_db",
        description="Directory for Chroma persistent storage"
    )
    
    # Retrieval
    retrieval_k: int = Field(
        default=3,
        ge=1,
        le=20,
        description="Number of documents to retrieve"
    )
    retrieval_score_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for retrieval"
    )
    retrieval_search_type: Literal["similarity", "mmr", "similarity_score_threshold"] = Field(
        default="similarity",
        description="Retrieval search type"
    )
    
    # Sprint 3: Tool Calling Configuration
    enable_tool_calling: bool = Field(
        default=True,
        description="启用工具调用功能"
    )
    tool_calling_timeout: float = Field(
        default=30.0,
        ge=1.0,
        le=120.0,
        description="工具调用超时时间（秒）"
    )
    max_tool_calls_per_query: int = Field(
        default=5,
        ge=1,
        le=10,
        description="每次查询最多调用工具次数"
    )
    
    # Sprint 4: Memory Management Configuration
    # Redis Configuration
    redis_host: str = Field(
        default="localhost",
        description="Redis server host"
    )
    redis_port: int = Field(
        default=6379,
        ge=1,
        le=65535,
        description="Redis server port"
    )
    redis_db: int = Field(
        default=0,
        ge=0,
        le=15,
        description="Redis database number"
    )
    redis_password: Optional[str] = Field(
        default=None,
        description="Redis password (if required)"
    )
    
    # Session Management Configuration
    session_ttl: int = Field(
        default=60 * 60 * 24 * 7,  # 7天（秒）
        ge=60,
        description="Session time-to-live in seconds"
    )
    max_history_length: int = Field(
        default=100,
        ge=10,
        le=1000,
        description="Maximum number of messages in conversation history"
    )
    max_context_tokens: int = Field(
        default=4000,
        ge=1000,
        le=32000,
        description="Maximum tokens for conversation context"
    )
    context_compression_threshold: float = Field(
        default=0.8,
        ge=0.5,
        le=1.0,
        description="Context compression threshold (80% by default)"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Global configuration instance
config = NexusConfig()