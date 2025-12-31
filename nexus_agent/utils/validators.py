"""
Nexus Agent Input/Output Validators
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Validation result with details"""
    is_valid: bool
    reason: str
    action: str  # "allow", "block", "modify"


class InputValidator:
    """Validates user input for safety and appropriateness"""
    
    def __init__(self):
        # Patterns for prompt injection attempts
        self.prompt_injection_patterns = [
            r"(?i)(ignore|forget|disregard|skip).*previous.*instruction",
            r"(?i)(system|admin|root).*:.*you are now",
            r"(?i)new.*role.*:.*",
            r"(?i)###.*instruction.*###",
            r"(?i)override.*prompt",
            r"(?i)act as.*if.*you are",
            r"(?i)pretend.*you are.*not",
            r"(?i)bypass.*restriction",
            r"(?i)jailbreak",
        ]
        
        # Patterns for sensitive information requests
        self.sensitive_patterns = [
            r"(?i)(salary|compensation|pay|wage).*information",
            r"(?i)(personal.*data|private.*information|confidential)",
            r"(?i)(password|credential|secret|token)",
            r"(?i)(social.*security|ssn|identification)",
            r"(?i)(bank.*account|credit.*card|financial)",
            r"(?i)(home.*address|personal.*phone|personal.*email)",
        ]
        
        # Patterns for inappropriate content
        self.inappropriate_patterns = [
            r"(?i)(hack|crack|exploit|bypass).*system",
            r"(?i)(illegal|unlawful|criminal)",
            r"(?i)(harmful|dangerous|violent)",
            r"(?i)(discriminate|harass|bully)",
        ]
        
        # Work-related keywords that should be allowed
        self.work_keywords = [
            "work", "job", "company", "employee", "colleague", "team",
            "project", "task", "meeting", "deadline", "schedule",
            "policy", "procedure", "benefit", "training", "onboarding",
            "office", "department", "manager", "report", "document",
            "工作", "公司", "员工", "同事", "团队", "项目", "任务",
            "会议", "截止日期", "政策", "流程", "福利", "培训",
            "入职", "办公室", "部门", "经理", "报告", "文档"
        ]
    
    def validate_input(self, user_input: str) -> ValidationResult:
        """Validate user input against safety patterns"""
        if not user_input or not user_input.strip():
            return ValidationResult(
                is_valid=False,
                reason="输入为空",
                action="block"
            )
        
        # Check for prompt injection attempts
        for pattern in self.prompt_injection_patterns:
            if re.search(pattern, user_input):
                return ValidationResult(
                    is_valid=False,
                    reason="检测到潜在的提示注入攻击",
                    action="block"
                )
        
        # Check for sensitive information requests
        for pattern in self.sensitive_patterns:
            if re.search(pattern, user_input):
                return ValidationResult(
                    is_valid=False,
                    reason="请求涉及敏感信息",
                    action="block"
                )
        
        # Check for inappropriate content
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, user_input):
                return ValidationResult(
                    is_valid=False,
                    reason="请求包含不当内容",
                    action="block"
                )
        
        # Check if input is work-related
        if not self._is_work_related(user_input):
            return ValidationResult(
                is_valid=False,
                reason="请求与工作无关，请提出与工作相关的问题",
                action="block"
            )
        
        return ValidationResult(
            is_valid=True,
            reason="输入验证通过",
            action="allow"
        )
    
    def _is_work_related(self, text: str) -> bool:
        """Check if text contains work-related keywords"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.work_keywords)


class OutputValidator:
    """Validates agent output for safety and appropriateness"""
    
    def __init__(self):
        # Patterns that should not appear in agent responses
        self.forbidden_patterns = [
            r"(?i)(i am|我是).*(not|不是).*nexus",
            r"(?i)(forget|ignore|disregard).*instruction",
            r"(?i)(i can|我能).*(help|协助).*(hack|crack|attack|攻击)",
            r"(?i)(here's|这是).*(password|secret|token|key)",
            r"(?i)(personal.*information|私人信息).*:.*",
            r"(?i)(salary|薪资|工资).*:.*\d+",
        ]
        
        # Required patterns for maintaining persona
        self.required_patterns = [
            r"(?i)(nexus|助手|assistant)",
        ]
    
    def validate_output(self, agent_output: str) -> ValidationResult:
        """Validate agent output against safety patterns"""
        if not agent_output or not agent_output.strip():
            return ValidationResult(
                is_valid=False,
                reason="输出为空",
                action="block"
            )
        
        # Check for forbidden content
        for pattern in self.forbidden_patterns:
            if re.search(pattern, agent_output):
                return ValidationResult(
                    is_valid=False,
                    reason="输出包含不当内容",
                    action="block"
                )
        
        # Check if output maintains appropriate persona (for longer responses)
        if len(agent_output) > 50:  # Only check longer responses
            has_persona = any(re.search(pattern, agent_output) for pattern in self.required_patterns)
            if not has_persona and not self._is_appropriate_response(agent_output):
                return ValidationResult(
                    is_valid=False,
                    reason="输出未保持适当的助手角色",
                    action="block"
                )
        
        return ValidationResult(
            is_valid=True,
            reason="输出验证通过",
            action="allow"
        )
    
    def _is_appropriate_response(self, text: str) -> bool:
        """Check if response is appropriate even without explicit persona mentions"""
        appropriate_indicators = [
            "抱歉", "无法", "不能", "建议", "请", "谢谢", "帮助",
            "policy", "政策", "流程", "部门", "联系", "咨询"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in appropriate_indicators)


class MessageHandler:
    """Combines input and output validation with message processing"""
    
    def __init__(self, enable_safety_checks: bool = True):
        self.enable_safety_checks = enable_safety_checks
        self.input_validator = InputValidator()
        self.output_validator = OutputValidator()
    
    def validate_input(self, user_input: str) -> bool:
        """Validate user input, return True if valid"""
        if not self.enable_safety_checks:
            return True
        
        result = self.input_validator.validate_input(user_input)
        return result.is_valid
    
    def validate_output(self, agent_output: str) -> bool:
        """Validate agent output, return True if valid"""
        if not self.enable_safety_checks:
            return True
        
        result = self.output_validator.validate_output(agent_output)
        return result.is_valid
    
    def get_validation_details(self, content: str, is_input: bool = True) -> ValidationResult:
        """Get detailed validation result"""
        if is_input:
            return self.input_validator.validate_input(content)
        else:
            return self.output_validator.validate_output(content)