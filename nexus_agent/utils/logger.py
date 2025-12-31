"""
Nexus Agent Logging Utilities
"""

import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from rich.logging import RichHandler
from rich.console import Console


class NexusLogger:
    """Structured logging for Nexus Agent"""
    
    def __init__(self, name: str = "nexus", log_file: Optional[str] = None, log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup console handler with Rich
        console = Console(stderr=True)
        console_handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True
        )
        
        console_formatter = logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Setup file handler if specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def log_conversation(self, user_input: str, agent_response: str, metadata: Dict[str, Any] = None):
        """Log conversation with structured data"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "conversation",
            "user_input": user_input,
            "agent_response": agent_response,
            "metadata": metadata or {}
        }
        self.logger.info(f"🗣️ CONVERSATION: {json.dumps(log_entry, ensure_ascii=False, indent=2)}")
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with context"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        }
        self.logger.error(f"❌ ERROR: {json.dumps(log_entry, ensure_ascii=False, indent=2)}")
    
    def log_llm_call(self, messages: list, response: str, tokens_used: Dict[str, int] = None, duration: float = None):
        """Log LLM API call details"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "llm_call",
            "message_count": len(messages),
            "response_length": len(response),
            "tokens_used": tokens_used or {},
            "duration_seconds": duration
        }
        self.logger.info(f"🤖 LLM_CALL: {json.dumps(log_entry, ensure_ascii=False, indent=2)}")
    
    def log_safety_violation(self, violation_type: str, content: str, action: str):
        """Log safety violations"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "safety_violation",
            "violation_type": violation_type,
            "content": content[:100] + "..." if len(content) > 100 else content,
            "action_taken": action
        }
        self.logger.warning(f"⚠️ SAFETY: {json.dumps(log_entry, ensure_ascii=False, indent=2)}")
    
    def log_system_event(self, event: str, details: Dict[str, Any] = None):
        """Log system events"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "system",
            "event": event,
            "details": details or {}
        }
        self.logger.info(f"🔧 SYSTEM: {json.dumps(log_entry, ensure_ascii=False, indent=2)}")
    
    def debug(self, message: str, **kwargs):
        """Debug level logging"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Info level logging"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Warning level logging"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Error level logging"""
        self.logger.error(message, extra=kwargs)


# Global logger instance
def get_logger(name: str = "nexus") -> NexusLogger:
    """Get or create a logger instance"""
    return NexusLogger(name)