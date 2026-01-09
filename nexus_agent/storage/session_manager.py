"""
会话管理器 - Sprint 4
管理用户会话和对话历史
"""

import uuid
from typing import Dict, Optional, List
from datetime import datetime
from .redis_client import get_redis_client


class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        """初始化会话管理器"""
        self.redis = get_redis_client()
    
    def create_session(
        self,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        创建新会话
        
        Args:
            user_id: 用户 ID（可选）
            metadata: 会话元数据（可选）
            
        Returns:
            会话 ID
        """
        # 生成唯一会话 ID
        session_id = str(uuid.uuid4())
        
        # 创建会话数据
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "message_count": 0,
            "metadata": metadata or {}
        }
        
        # 保存到 Redis
        self.redis.save_session(session_id, session_data)
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        获取会话信息
        
        Args:
            session_id: 会话 ID
            
        Returns:
            会话信息
        """
        return self.redis.get_session(session_id)
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """
        更新会话信息
        
        Args:
            session_id: 会话 ID
            **kwargs: 要更新的字段
            
        Returns:
            是否更新成功
        """
        session_data = self.redis.get_session(session_id)
        if not session_data:
            return False
        
        # 更新字段
        for key, value in kwargs.items():
            session_data[key] = value
        
        # 保存更新
        return self.redis.save_session(session_id, session_data)
    
    def increment_message_count(self, session_id: str) -> bool:
        """
        增加消息计数
        
        Args:
            session_id: 会话 ID
            
        Returns:
            是否更新成功
        """
        session_data = self.redis.get_session(session_id)
        if not session_data:
            return False
        
        session_data["message_count"] = session_data.get("message_count", 0) + 1
        session_data["last_active"] = datetime.now().isoformat()
        
        return self.redis.save_session(session_id, session_data)
    
    def delete_session(self, session_id: str) -> bool:
        """
        删除会话
        
        Args:
            session_id: 会话 ID
            
        Returns:
            是否删除成功
        """
        return self.redis.delete_session(session_id)
    
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """
        获取用户的所有会话
        
        Args:
            user_id: 用户 ID
            
        Returns:
            会话列表
        """
        all_sessions = self.redis.get_all_sessions()
        return [
            session for session in all_sessions
            if session.get("user_id") == user_id
        ]
    
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
        return self.redis.get_conversation_history(session_id, limit)
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        添加消息到对话历史
        
        Args:
            session_id: 会话 ID
            role: 角色 (user/assistant/system)
            content: 消息内容
            metadata: 元数据（可选）
            
        Returns:
            是否添加成功
        """
        # 添加消息
        success = self.redis.add_message(session_id, role, content, metadata)
        
        if success:
            # 更新消息计数
            self.increment_message_count(session_id)
        
        return success
    
    def clear_history(self, session_id: str) -> bool:
        """
        清空对话历史
        
        Args:
            session_id: 会话 ID
            
        Returns:
            是否清空成功
        """
        return self.redis.clear_history(session_id)
