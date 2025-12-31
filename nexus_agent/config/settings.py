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
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Global configuration instance
config = NexusConfig()