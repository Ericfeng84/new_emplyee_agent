"""
上下文管理器 - Sprint 4
管理对话上下文和 Token 预算
"""

import tiktoken
from typing import List, Dict, Optional, Tuple
from nexus_agent.config.settings import config


class ContextManager:
    """上下文管理器"""
    
    def __init__(self):
        """初始化上下文管理器"""
        # 初始化 tokenizer（使用 GPT-4 的编码）
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4")
        except:
            # 如果无法获取，使用默认编码
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """
        计算文本的 Token 数量
        
        Args:
            text: 输入文本
            
        Returns:
            Token 数量
        """
        return len(self.encoding.encode(text))
    
    def count_messages_tokens(self, messages: List[Dict]) -> int:
        """
        计算消息列表的 Token 数量
        
        Args:
            messages: 消息列表
            
        Returns:
            总 Token 数量
        """
        total_tokens = 0
        
        for message in messages:
            # 每条消息有固定的开销（约 4 tokens）
            total_tokens += 4
            
            # 计算角色和内容的 tokens
            for key, value in message.items():
                if isinstance(value, str):
                    total_tokens += self.count_tokens(value)
                elif isinstance(value, dict):
                    # 处理元数据等字典类型
                    total_tokens += self.count_tokens(str(value))
        
        # 添加回复前缀的开销
        total_tokens += 3
        
        return total_tokens
    
    def check_token_budget(
        self,
        messages: List[Dict],
        max_tokens: Optional[int] = None
    ) -> Tuple[bool, int]:
        """
        检查是否超出 Token 预算
        
        Args:
            messages: 消息列表
            max_tokens: 最大 Token 数（默认使用配置）
            
        Returns:
            (是否超限, 当前 Token 数)
        """
        if max_tokens is None:
            max_tokens = config.max_context_tokens
        
        current_tokens = self.count_messages_tokens(messages)
        is_over_budget = current_tokens > max_tokens
        
        return is_over_budget, current_tokens
    
    def compress_context(
        self,
        messages: List[Dict],
        max_tokens: Optional[int] = None
    ) -> List[Dict]:
        """
        压缩上下文以适应 Token 预算
        
        策略：
        1. 保留最近的 N 条消息
        2. 如果还是超限，生成摘要
        
        Args:
            messages: 原始消息列表
            max_tokens: 最大 Token 数（默认使用配置）
            
        Returns:
            压缩后的消息列表
        """
        if max_tokens is None:
            max_tokens = config.max_context_tokens
        
        # 检查是否需要压缩
        is_over_budget, current_tokens = self.check_token_budget(messages, max_tokens)
        
        if not is_over_budget:
            return messages
        
        print(f"⚠️  上下文超限: {current_tokens} tokens > {max_tokens} tokens")
        print("🔄 开始压缩上下文...")
        
        # 策略 1: 保留最近的 N 条消息
        compressed = self._keep_recent_messages(messages, max_tokens)
        
        # 检查是否还需要进一步压缩
        is_over_budget, new_tokens = self.check_token_budget(compressed, max_tokens)
        
        if is_over_budget:
            # 策略 2: 生成摘要（简化版：只保留最关键的消息）
            compressed = self._generate_summary(compressed, max_tokens)
        
        final_tokens = self.count_messages_tokens(compressed)
        print(f"✅ 压缩完成: {current_tokens} -> {final_tokens} tokens")
        
        return compressed
    
    def _keep_recent_messages(
        self,
        messages: List[Dict],
        max_tokens: int
    ) -> List[Dict]:
        """
        保留最近的 N 条消息
        
        Args:
            messages: 原始消息列表
            max_tokens: 最大 Token 数
            
        Returns:
            保留的消息列表
        """
        # 从最近的开始，逐步添加直到接近预算
        result = []
        
        # 从后往前遍历（保留最新的消息）
        for message in reversed(messages):
            # 临时添加这条消息
            temp = [message] + result
            tokens = self.count_messages_tokens(temp)
            
            if tokens <= max_tokens:
                result = temp
            else:
                break
        
        return result
    
    def _generate_summary(
        self,
        messages: List[Dict],
        max_tokens: int
    ) -> List[Dict]:
        """
        生成摘要（简化版：只保留最关键的消息）
        
        Args:
            messages: 原始消息列表
            max_tokens: 最大 Token 数
            
        Returns:
            摘要后的消息列表
        """
        # 保留系统消息（如果有）
        system_messages = [m for m in messages if m.get("role") == "system"]
        
        # 保留最近的几条用户和助手消息
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        
        # 合并
        result = system_messages + recent_messages
        
        # 如果还是超限，只保留最近的消息
        is_over_budget, _ = self.check_token_budget(result, max_tokens)
        if is_over_budget:
            result = result[-5:]  # 只保留最近 5 条
        
        return result
    
    def format_messages_for_llm(
        self,
        messages: List[Dict]
    ) -> List[Dict]:
        """
        格式化消息以供 LLM 使用
        
        Args:
            messages: 原始消息列表
            
        Returns:
            格式化后的消息列表
        """
        # 过滤掉元数据等不需要的字段
        formatted = []
        
        for message in messages:
            formatted_msg = {
                "role": message.get("role"),
                "content": message.get("content")
            }
            formatted.append(formatted_msg)
        
        return formatted
    
    def get_context_stats(self, messages: List[Dict]) -> Dict:
        """
        获取上下文统计信息
        
        Args:
            messages: 消息列表
            
        Returns:
            统计信息字典
        """
        total_tokens = self.count_messages_tokens(messages)
        message_count = len(messages)
        
        # 按角色统计
        role_counts = {}
        for message in messages:
            role = message.get("role", "unknown")
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return {
            "total_tokens": total_tokens,
            "message_count": message_count,
            "role_counts": role_counts,
            "is_over_budget": total_tokens > config.max_context_tokens,
            "budget_ratio": total_tokens / config.max_context_tokens
        }
