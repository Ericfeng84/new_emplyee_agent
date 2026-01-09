"""
Main Nexus Agent implementation using LangChain's create_agent
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from ..config.settings import config
from ..utils.logger import get_logger
from .state import NexusAgentState
from .tools import NEXUS_TOOLS
from .api_tools import API_TOOLS
from .middleware import (
    SafetyMiddleware,
    NexusModelSelectionMiddleware,
    NexusPromptMiddleware,
    ToolErrorMiddleware
)
from .prompts import BASE_SYSTEM_PROMPT
from ..storage.session_manager import SessionManager
from ..storage.context_manager import ContextManager


@dataclass
class AgentResponse:
    """Standard response from Nexus Agent"""
    content: str
    success: bool
    error: Optional[str] = None
    tokens_used: Optional[Dict[str, int]] = None
    duration: Optional[float] = None
    context_id: Optional[str] = None
    session_id: Optional[str] = None  # Sprint 4: 添加 session_id
    metadata: Optional[Dict[str, Any]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class NexusLangChainAgent:
    """
    Nexus Agent using LangChain's create_agent
    
    Optimized implementation with:
    - Tool calling for work-related queries
    - Middleware for safety checks
    - Dynamic model selection
    - Custom state management
    """
    
    def __init__(self,
                 provider: str = None,
                 model: str = None,
                 temperature: float = None,
                 enable_safety_checks: bool = True,
                 enable_memory: bool = False):  # Sprint 4: 新增记忆管理参数
        
        # Configuration
        self.provider = provider or config.llm_provider
        self.model = model or config.llm_model
        self.temperature = temperature if temperature is not None else config.temperature
        self.enable_safety_checks = enable_safety_checks
        self.enable_memory = enable_memory  # Sprint 4: 记忆功能开关
        
        # Initialize logger
        self.logger = get_logger("nexus_langchain_agent")
        
        # Initialize tools - merge existing tools with API tools
        self.tools = NEXUS_TOOLS + API_TOOLS
        
        # Initialize middleware
        self.middleware = []
        
        # Add safety middleware if enabled
        if self.enable_safety_checks:
            self.safety_middleware = SafetyMiddleware(enable_safety_checks=True)
            self.middleware.append(self.safety_middleware)
        
        # Add model selection middleware
        self.model_selection = NexusModelSelectionMiddleware()
        self.middleware.append(self.model_selection)
        
        # Add prompt middleware
        self.prompt_middleware = NexusPromptMiddleware()
        self.middleware.append(self.prompt_middleware)
        
        # Add tool error middleware
        self.tool_error_middleware = ToolErrorMiddleware()
        self.middleware.append(self.tool_error_middleware)
        
        # Initialize base model
        self.base_model = self._get_model()
        
        # Create the agent
        self.agent = create_agent(
            model=self.base_model,
            tools=self.tools,
            state_schema=NexusAgentState,
            middleware=self.middleware,
            system_prompt=BASE_SYSTEM_PROMPT
        )
        
        # Initialize default context
        self.default_context_id = "default_conversation"
        
        # Sprint 4: 初始化记忆管理
        if self.enable_memory:
            self.session_manager = SessionManager()
            self.context_manager = ContextManager()
            self.logger.log_system_event("memory_enabled", {
                "redis_host": config.redis_host,
                "redis_port": config.redis_port,
                "max_context_tokens": config.max_context_tokens
            })
        else:
            self.session_manager = None
            self.context_manager = None
        
        self.logger.log_system_event("agent_initialized", {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "safety_checks": self.enable_safety_checks,
            "tools_count": len(self.tools),
            "memory_enabled": self.enable_memory
        })
    
    def _get_model(self) -> ChatOpenAI:
        """Get the base model based on provider"""
        if self.provider == "openai":
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                openai_api_key=config.openai_api_key
            )
        elif self.provider == "deepseek":
            return ChatOpenAI(
                model=self.model or "deepseek-chat",
                temperature=self.temperature,
                openai_api_key=config.deepseek_api_key,
                openai_api_base="https://api.deepseek.com"
            )
        elif self.provider == "qwen":
            return ChatOpenAI(
                model=self.model or "qwen-plus",
                temperature=self.temperature,
                openai_api_key=config.qwen_api_key,
                openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def process_message(self,
                       user_input: str,
                       context_id: str = None,
                       user_id: str = None,
                       session_id: str = None,  # Sprint 4: 新增 session_id 参数
                       user_preferences: Dict[str, Any] = None) -> AgentResponse:
        """
        Process a user message and generate a response
        
        Args:
            user_input: The user's input message
            context_id: Optional conversation context ID
            user_id: Optional user ID for session management
            session_id: Optional session ID for memory management
            user_preferences: Optional user preferences for context
            
        Returns:
            AgentResponse with the agent's response
        """
        import time
        
        start_time = time.time()
        
        # Sprint 4: 记忆管理
        history = []
        if self.enable_memory:
            # 如果没有 session_id，创建新会话
            if not session_id:
                session_id = self.session_manager.create_session(user_id=user_id)
            
            # 加载历史对话
            history = self.session_manager.get_conversation_history(session_id)
            
            # 上下文压缩
            if history:
                history = self.context_manager.compress_context(history)
        
        # Use default context if none provided
        if context_id is None:
            context_id = self.default_context_id
        
        # Prepare input state
        input_state = {
            "messages": self._build_messages(user_input, history),  # Sprint 4: 使用历史消息
            "user_id": user_id or "default",
            "session_id": session_id or context_id,
            "user_preferences": user_preferences or {},
            "conversation_stats": {}
        }
        
        response = AgentResponse(
            content="",
            success=False,
            context_id=context_id,
            session_id=session_id  # Sprint 4: 返回 session_id
        )
        
        try:
            # Invoke the agent
            result = self.agent.invoke(input_state)
            
            # Extract response
            messages = result.get("messages", [])
            if messages:
                last_message = messages[-1]
                response.content = last_message.content
                
                # Extract tool calls if present
                tool_calls = []
                for msg in messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        tool_calls.extend(msg.tool_calls)
                response.tool_calls = tool_calls
            
            response.success = True
            response.duration = time.time() - start_time
            response.metadata = {
                "provider": self.provider,
                "model": self.model,
                "context_id": context_id,
                "session_id": session_id
            }
            
            # Sprint 4: 保存到历史
            if self.enable_memory and session_id:
                # 保存用户消息
                self.session_manager.add_message(
                    session_id,
                    role="user",
                    content=user_input
                )
                
                # 保存助手响应
                self.session_manager.add_message(
                    session_id,
                    role="assistant",
                    content=response.content,
                    metadata={
                        "tool_calls": response.tool_calls,
                        "duration": response.duration
                    }
                )
            
            # Log conversation
            self.logger.log_conversation(
                user_input=user_input,
                agent_response=response.content,
                metadata={
                    "context_id": context_id,
                    "session_id": session_id,
                    "duration": response.duration,
                    "tool_calls_count": len(response.tool_calls) if response.tool_calls else 0
                }
            )
            
            return response
            
        except Exception as e:
            self.logger.log_error(e, {
                "context_id": context_id,
                "session_id": session_id,
                "user_input": user_input
            })
            
            response.error = str(e)
            response.content = "抱歉，处理您的请求时遇到了问题。请稍后重试或联系技术支持。"
            response.duration = time.time() - start_time
            
            return response
    
    def stream_message(self,
                      user_input: str,
                      context_id: str = None,
                      user_preferences: Dict[str, Any] = None):
        """
        Stream responses from the agent
        
        Args:
            user_input: The user's input message
            context_id: Optional conversation context ID
            user_preferences: Optional user preferences for context
            
        Yields:
            Chunks of the agent's response
        """
        # Use default context if none provided
        if context_id is None:
            context_id = self.default_context_id
        
        # Prepare input state
        input_state = {
            "messages": [HumanMessage(content=user_input)],
            "user_id": "default",
            "session_id": context_id,
            "user_preferences": user_preferences or {},
            "conversation_stats": {}
        }
        
        try:
            for chunk in self.agent.stream(input_state, stream_mode="values"):
                latest_message = chunk["messages"][-1]
                if latest_message.content:
                    yield {
                        "content": latest_message.content,
                        "type": "message"
                    }
                elif hasattr(latest_message, 'tool_calls') and latest_message.tool_calls:
                    yield {
                        "tool_calls": latest_message.tool_calls,
                        "type": "tool_calls"
                    }
        except Exception as e:
            self.logger.log_error(e, {
                "context_id": context_id,
                "user_input": user_input
            })
            yield {
                "error": str(e),
                "type": "error"
            }
    
    def chat(self, message: str, user_preferences: Dict[str, Any] = None) -> str:
        """Simple chat interface for quick interactions"""
        response = self.process_message(message, user_preferences=user_preferences)
        return response.content if response.success else response.error
    
    def interactive_chat(self):
        """Start an interactive chat session"""
        from rich.console import Console
        from rich.panel import Panel
        
        console = Console()
        
        console.print(Panel.fit(
            "[bold cyan]Nexus Agent - 新员工入职助手[/bold cyan]\n"
            "[dim]输入 'quit' 或 'exit' 退出对话[/dim]",
            title="欢迎使用",
            border_style="cyan"
        ))
        
        while True:
            try:
                # Get user input
                user_input = console.input("\n[bold green]你:[/bold green] ")
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', '退出']:
                    console.print("[yellow]再见！祝您工作顺利！[/yellow]")
                    break
                
                # Process message
                response = self.process_message(user_input)
                
                # Display response
                if response.success:
                    console.print(f"\n[bold cyan]Nexus:[/bold cyan] {response.content}")
                    
                    if response.tool_calls:
                        console.print(f"[dim]使用了 {len(response.tool_calls)} 个工具[/dim]")
                    
                    if response.duration:
                        console.print(f"[dim]Duration: {response.duration:.2f}s[/dim]")
                else:
                    console.print(f"\n[red]错误: {response.error}[/red]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]对话已中断。再见！[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]发生错误: {str(e)}[/red]")
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent configuration"""
        return {
            "type": "langchain_agent",
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "safety_checks": self.enable_safety_checks,
            "tools": [tool.name for tool in self.tools],
            "middleware_count": len(self.middleware)
        }
    
    def _build_messages(
        self,
        user_message: str,
        history: List[Dict] = None
    ) -> List:
        """
        构建消息列表
        
        Args:
            user_message: 用户消息
            history: 历史消息（可选）
            
        Returns:
            消息列表
        """
        messages = []
        
        # 添加系统提示词
        messages.append(HumanMessage(content=BASE_SYSTEM_PROMPT))
        
        # 添加历史消息
        if history:
            for msg in history:
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(HumanMessage(content=content))  # 使用 HumanMessage 作为临时方案
                elif role == "system":
                    messages.append(HumanMessage(content=content))
        
        # 添加当前用户消息
        messages.append(HumanMessage(content=user_message))
        
        return messages
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        获取会话信息
        
        Args:
            session_id: 会话 ID
            
        Returns:
            会话信息
        """
        if not self.enable_memory or not self.session_manager:
            return None
        
        return self.session_manager.get_session(session_id)
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        获取对话历史
        
        Args:
            session_id: 会话 ID
            limit: 限制返回的消息数量（可选）
            
        Returns:
            消息列表
        """
        if not self.enable_memory or not self.session_manager:
            return []
        
        return self.session_manager.get_conversation_history(session_id, limit)
    
    def clear_session(self, session_id: str) -> bool:
        """
        清空会话历史
        
        Args:
            session_id: 会话 ID
            
        Returns:
            是否清空成功
        """
        if not self.enable_memory or not self.session_manager:
            return False
        
        return self.session_manager.clear_history(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """
        删除会话
        
        Args:
            session_id: 会话 ID
            
        Returns:
            是否删除成功
        """
        if not self.enable_memory or not self.session_manager:
            return False
        
        return self.session_manager.delete_session(session_id)
    
    def test_connection(self) -> bool:
        """Test if the agent is working"""
        try:
            response = self.process_message("你好，请简单介绍一下自己。")
            return response.success
        except Exception as e:
            self.logger.log_error(e, {"test_connection": True})
            return False


# Convenience function for quick agent creation
def create_nexus_agent(**kwargs) -> NexusLangChainAgent:
    """Create a Nexus Agent with default or custom configuration"""
    return NexusLangChainAgent(**kwargs)
