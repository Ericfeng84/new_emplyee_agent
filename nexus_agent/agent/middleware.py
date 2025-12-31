"""
Middleware for Nexus Agent
Safety checks, model selection, dynamic prompts, and error handling
"""

from typing import Optional, Dict, Any
from langchain.agents.middleware import (
    wrap_tool_call,
    wrap_model_call,
    dynamic_prompt,
    ModelRequest,
    ModelResponse,
    AgentMiddleware
)
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

from ..config.settings import config
from ..utils.logger import get_logger
from ..utils.validators import MessageHandler as BaseMessageHandler
from .state import NexusAgentState


class SafetyMiddleware(AgentMiddleware):
    """Middleware for safety checks and validation"""
    
    def __init__(self, enable_safety_checks: bool = True):
        super().__init__()
        self.enable_safety_checks = enable_safety_checks
        self.logger = get_logger("safety_middleware")
        self.validator = BaseMessageHandler(enable_safety_checks=enable_safety_checks)
    
    def before_model(self, state: NexusAgentState, runtime) -> Optional[Dict[str, Any]]:
        """Validate input before model call"""
        if not self.enable_safety_checks:
            return None
        
        # Get the latest user message
        messages = state.get("messages", [])
        if not messages:
            return None
        
        last_message = messages[-1]
        if isinstance(last_message, HumanMessage):
            validation_result = self.validator.get_validation_details(
                last_message.content,
                is_input=True
            )
            
            if not validation_result.is_valid:
                self.logger.log_safety_violation(
                    "input_validation",
                    last_message.content,
                    validation_result.action
                )
                
                # Return a response that will be used instead of calling the model
                return {
                    "skip_model": True,
                    "safety_violation": True,
                    "response": "抱歉，我无法处理这个请求。请提出与工作相关的问题。"
                }
        
        return None


class NexusModelSelectionMiddleware(AgentMiddleware):
    """Middleware for dynamic model selection based on conversation complexity"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("model_selection")
        
        # Initialize models for different providers
        self.models = {
            "openai": ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                openai_api_key=config.openai_api_key
            ),
            "deepseek": ChatOpenAI(
                model="deepseek-chat",
                temperature=0.7,
                openai_api_key=config.deepseek_api_key,
                openai_api_base="https://api.deepseek.com"
            ),
            "qwen": ChatOpenAI(
                model="qwen-plus",
                temperature=0.7,
                openai_api_key=config.qwen_api_key,
                openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        }
        
        self.current_provider = config.llm_provider
    
    def select_model(self, request: ModelRequest, handler) -> ModelResponse:
        """Select model based on conversation state"""
        message_count = len(request.state.get("messages", []))
        
        # Use more advanced model for longer conversations
        if message_count > 10:
            # For longer conversations, prefer higher quality model
            if self.current_provider == "openai":
                model = ChatOpenAI(
                    model="gpt-4o",
                    temperature=0.7,
                    openai_api_key=config.openai_api_key
                )
            else:
                model = self.models[self.current_provider]
        else:
            model = self.models[self.current_provider]
        
        self.logger.log_system_event("model_selected", {
            "provider": self.current_provider,
            "message_count": message_count,
            "model": model.model_name if hasattr(model, 'model_name') else model.model
        })
        
        return handler(request.override(model=model))
    
    select_model = wrap_model_call(select_model)


class NexusPromptMiddleware(AgentMiddleware):
    """Middleware for dynamic prompt generation"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("prompt_middleware")
        self.base_prompt = self._get_base_system_prompt()
    
    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt"""
        return """
你是一个名为 Nexus 的智能助手，专门为公司新员工提供入职支持和工作协助。

## 你的角色定位
- **身份**: 公司内部 AI 助手，专注于新员工入职体验
- **语气**: 专业、热情、耐心、友好
- **边界**: 只回答与工作相关的问题，不涉及个人隐私或敏感信息

## 你的核心能力
1. **知识解答**: 回答关于公司政策、流程、制度的问题
2. **工作协助**: 提供日常工作中的指导和帮助
3. **资源指引**: 引导员工找到正确的信息和联系人

## 交互原则
- 始终保持专业和礼貌的语气
- 如果不确定答案，诚实说明并建议联系相关部门
- 不处理涉及薪资、个人隐私等敏感信息的请求
- 鼓励新员工提出问题，营造支持性的氛围
- 使用中文进行交流，保持简洁明了的表达

## 安全边界
- 拒绝回答非工作相关问题
- 不存储或处理个人敏感信息
- 遇到不当请求时，礼貌地引导回工作话题
- 不参与任何可能危害公司安全的讨论

## 可用工具
你有以下工具可以使用：
- lookup_company_policy: 查询公司政策和流程
- get_contact_info: 获取部门联系方式
- search_knowledge_base: 搜索公司知识库
- get_onboarding_guide: 获取新员工入职指南

请记住：你的目标是帮助新员工快速适应工作环境，提高工作效率。
"""
    
    def generate_prompt(self, request: ModelRequest) -> str:
        """Generate dynamic system prompt based on context"""
        user_preferences = request.runtime.context.get("user_preferences", {})
        user_role = user_preferences.get("role", "new_employee")
        
        prompt = self.base_prompt
        
        # Customize based on user role
        if user_role == "new_employee":
            prompt += "\n\n## 特别说明\n用户是新员工，请提供更详细和耐心的解释，帮助他们快速了解公司。"
        elif user_role == "manager":
            prompt += "\n\n## 特别说明\n用户是管理者，请提供更简洁和专业的回答，关注管理层面的信息。"
        
        return prompt
    
    generate_prompt = dynamic_prompt(generate_prompt)


class ToolErrorMiddleware(AgentMiddleware):
    """Middleware for handling tool errors"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("tool_error_middleware")
    
    def handle_tool_errors(self, request, handler):
        """Handle tool execution errors with custom messages"""
        try:
            return handler(request)
        except Exception as e:
            self.logger.log_error(e, {
                "tool_name": request.tool_call.get("name"),
                "tool_args": request.tool_call.get("args")
            })
            
            # Return a user-friendly error message
            return ToolMessage(
                content=f"抱歉，处理您的请求时遇到了问题。请稍后重试或尝试其他方式获取信息。",
                tool_call_id=request.tool_call["id"]
            )
    
    handle_tool_errors = wrap_tool_call(handle_tool_errors)
