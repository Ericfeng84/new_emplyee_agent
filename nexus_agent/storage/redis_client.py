"""
Redis 客户端 - Sprint 4
用于持久化存储对话历史和会话信息
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import redis
from redis.connection import ConnectionPool
from nexus_agent.config.settings import config


class RedisClient:
    """Redis 客户端封装"""
    
    def __init__(self):
        """初始化 Redis 连接"""
        # 创建连接池
        self.pool = ConnectionPool(
            host=config.redis_host,
            port=config.redis_port,
            db=config.redis_db,
            password=config.redis_password,
            decode_responses=True,  # 自动解码为字符串
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
        
        # 创建 Redis 客户端
        self.client = redis.Redis(connection_pool=self.pool)
        
        # 测试连接
        try:
            self.client.ping()
            print("✅ Redis 连接成功")
        except Exception as e:
            print(f"❌ Redis 连接失败: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        获取会话信息
        
        Args:
            session_id: 会话 ID
            
        Returns:
            会话信息字典，如果不存在则返回 None
        """
        key = f"session:{session_id}"
        data = self.client.get(key)
        
        if data:
            return json.loads(data)
        return None
    
    def save_session(self, session_id: str, session_data: Dict) -> bool:
        """
        保存会话信息
        
        Args:
            session_id: 会话 ID
            session_data: 会话数据
            
        Returns:
            是否保存成功
        """
        key = f"session:{session_id}"
        try:
            # 设置过期时间（7天）
            self.client.setex(
                key,
                config.session_ttl,
                json.dumps(session_data, ensure_ascii=False)
            )
            return True
        except Exception as e:
            print(f"❌ 保存会话失败: {e}")
            return False
    
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
        key = f"history:{session_id}"
        
        try:
            # 获取所有消息
            messages = self.client.lrange(key, 0, -1)
            
            # 反转列表（Redis 返回的是从旧到新）
            messages = messages[::-1]
            
            # 解析 JSON
            history = [json.loads(msg) for msg in messages]
            
            # 应用限制
            if limit:
                history = history[-limit:]
            
            return history
        except Exception as e:
            print(f"❌ 获取对话历史失败: {e}")
            return []
    
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
        key = f"history:{session_id}"
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        try:
            # 添加到列表头部
            self.client.lpush(key, json.dumps(message, ensure_ascii=False))
            
            # 设置过期时间
            self.client.expire(key, config.session_ttl)
            
            # 限制历史长度
            max_length = config.max_history_length
            if max_length:
                self.client.ltrim(key, 0, max_length - 1)
            
            return True
        except Exception as e:
            print(f"❌ 添加消息失败: {e}")
            return False
    
    def clear_history(self, session_id: str) -> bool:
        """
        清空对话历史
        
        Args:
            session_id: 会话 ID
            
        Returns:
            是否清空成功
        """
        key = f"history:{session_id}"
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"❌ 清空历史失败: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        删除会话
        
        Args:
            session_id: 会话 ID
            
        Returns:
            是否删除成功
        """
        try:
            # 删除会话信息
            self.client.delete(f"session:{session_id}")
            # 删除对话历史
            self.client.delete(f"history:{session_id}")
            return True
        except Exception as e:
            print(f"❌ 删除会话失败: {e}")
            return False
    
    def get_all_sessions(self) -> List[Dict]:
        """
        获取所有会话列表
        
        Returns:
            会话列表
        """
        try:
            # 获取所有 session key
            keys = self.client.keys("session:*")
            
            sessions = []
            for key in keys:
                session_id = key.split(":")[1]
                session_data = self.get_session(session_id)
                if session_data:
                    sessions.append({
                        "session_id": session_id,
                        **session_data
                    })
            
            return sessions
        except Exception as e:
            print(f"❌ 获取会话列表失败: {e}")
            return []
    
    def close(self):
        """关闭 Redis 连接"""
        try:
            self.pool.disconnect()
            print("✅ Redis 连接已关闭")
        except Exception as e:
            print(f"❌ 关闭 Redis 连接失败: {e}")


# 全局 Redis 客户端实例
redis_client = None


def get_redis_client() -> RedisClient:
    """
    获取 Redis 客户端实例（单例模式）
    
    Returns:
        RedisClient 实例
    """
    global redis_client
    if redis_client is None:
        redis_client = RedisClient()
    return redis_client
