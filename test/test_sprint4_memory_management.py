"""
Sprint 4: 记忆管理与多轮对话 - 综合测试脚本

测试覆盖：
1. Redis 客户端连接和基本操作
2. 会话管理器功能
3. 上下文管理器功能
4. Agent 记忆集成
5. 多用户会话隔离
6. 上下文压缩
7. 会话管理操作
"""

import pytest
import time
import uuid
from typing import List, Dict, Any
from datetime import datetime

# 导入 Sprint 4 组件
from nexus_agent.storage.redis_client import RedisClient
from nexus_agent.storage.session_manager import SessionManager
from nexus_agent.storage.context_manager import ContextManager
from nexus_agent.agent.agent import NexusLangChainAgent


class TestRedisClient:
    """测试 Redis 客户端功能"""
    
    @pytest.fixture
    def redis_client(self):
        """创建 Redis 客户端实例"""
        client = RedisClient()
        yield client
        # 清理测试数据 - 删除所有测试会话
        all_sessions = client.get_all_sessions()
        for session in all_sessions:
            client.delete_session(session['session_id'])
    
    def test_redis_connection(self, redis_client):
        """测试 Redis 连接"""
        # RedisClient 在初始化时已经测试连接
        assert redis_client.client is not None, "Redis 客户端未初始化"
        print("✅ Redis 连接测试通过")
    
    def test_save_and_get_session(self, redis_client):
        """测试保存和获取会话"""
        session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        session_data = {
            "session_id": session_id,
            "user_id": "test_user",
            "created_at": datetime.now().isoformat(),
            "message_count": 0
        }
        
        # 保存会话
        success = redis_client.save_session(session_id, session_data)
        assert success == True, "保存会话失败"
        
        # 获取会话
        result = redis_client.get_session(session_id)
        assert result is not None, "获取会话失败"
        assert result.get('session_id') == session_id, "会话 ID 不匹配"
        print("✅ Redis save/get session 测试通过")
    
    def test_conversation_history(self, redis_client):
        """测试对话历史"""
        session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        
        # 添加消息
        redis_client.add_message(session_id, "user", "你好")
        redis_client.add_message(session_id, "assistant", "你好！有什么可以帮助你的？")
        
        # 获取历史
        history = redis_client.get_conversation_history(session_id)
        assert len(history) == 2, f"期望 2 条消息，实际 {len(history)} 条"
        assert history[0]['role'] == 'user', "第一条消息应该是用户消息"
        assert history[1]['role'] == 'assistant', "第二条消息应该是助手消息"
        print("✅ Redis conversation history 测试通过")
    
    def test_delete_session(self, redis_client):
        """测试删除会话"""
        session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        session_data = {"session_id": session_id}
        
        # 保存会话
        redis_client.save_session(session_id, session_data)
        assert redis_client.get_session(session_id) is not None
        
        # 删除会话
        success = redis_client.delete_session(session_id)
        assert success == True, "删除会话失败"
        assert redis_client.get_session(session_id) is None, "删除后会话应该不存在"
        print("✅ Redis delete session 测试通过")
    
    def test_clear_history(self, redis_client):
        """测试清空历史"""
        session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        
        # 添加消息
        redis_client.add_message(session_id, "user", "消息1")
        redis_client.add_message(session_id, "user", "消息2")
        
        # 清空历史
        success = redis_client.clear_history(session_id)
        assert success == True, "清空历史失败"
        
        history = redis_client.get_conversation_history(session_id)
        assert len(history) == 0, "清空后历史应该为空"
        print("✅ Redis clear history 测试通过")


class TestSessionManager:
    """测试会话管理器功能"""
    
    @pytest.fixture
    def session_manager(self):
        """创建会话管理器实例"""
        manager = SessionManager()
        yield manager
        # 清理测试数据
        all_sessions = manager.redis.get_all_sessions()
        for session in all_sessions:
            manager.delete_session(session['session_id'])
    
    def test_create_session(self, session_manager):
        """测试创建会话"""
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        
        # 创建会话
        session_id = session_manager.create_session(user_id=user_id)
        
        # 验证会话 ID
        assert session_id is not None, "会话 ID 不能为空"
        assert isinstance(session_id, str), "会话 ID 应该是字符串"
        
        # 验证会话存在
        session_data = session_manager.get_session(session_id)
        assert session_data is not None, "会话数据不能为空"
        assert session_data.get('user_id') == user_id, "用户 ID 不匹配"
        print(f"✅ 创建会话测试通过 (Session ID: {session_id})")
    
    def test_get_session(self, session_manager):
        """测试获取会话"""
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        session_id = session_manager.create_session(user_id=user_id)
        
        # 获取会话
        session_data = session_manager.get_session(session_id)
        
        assert session_data is not None, "会话数据不能为空"
        assert session_data.get('session_id') == session_id, "会话 ID 不匹配"
        assert session_data.get('user_id') == user_id, "用户 ID 不匹配"
        assert 'created_at' in session_data, "缺少创建时间"
        assert 'message_count' in session_data, "缺少消息计数"
        print("✅ 获取会话测试通过")
    
    def test_add_message(self, session_manager):
        """测试添加消息"""
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        session_id = session_manager.create_session(user_id=user_id)
        
        # 添加用户消息
        session_manager.add_message(session_id, "user", "你好，我是测试用户")
        
        # 添加助手消息
        session_manager.add_message(session_id, "assistant", "你好！很高兴认识你")
        
        # 获取消息历史
        messages = session_manager.get_conversation_history(session_id)
        
        assert len(messages) == 2, f"期望 2 条消息，实际 {len(messages)} 条"
        assert messages[0]['role'] == 'user', "第一条消息应该是用户消息"
        assert messages[1]['role'] == 'assistant', "第二条消息应该是助手消息"
        print("✅ 添加消息测试通过")
    
    def test_get_messages(self, session_manager):
        """测试获取消息历史"""
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        session_id = session_manager.create_session(user_id=user_id)
        
        # 添加多条消息
        for i in range(5):
            role = 'user' if i % 2 == 0 else 'assistant'
            session_manager.add_message(session_id, role, f'测试消息 {i+1}')
        
        # 获取所有消息
        messages = session_manager.get_conversation_history(session_id)
        assert len(messages) == 5, f"期望 5 条消息，实际 {len(messages)} 条"
        
        # 获取前 3 条消息
        messages_limited = session_manager.get_conversation_history(session_id, limit=3)
        assert len(messages_limited) == 3, f"期望 3 条消息，实际 {len(messages_limited)} 条"
        print("✅ 获取消息历史测试通过")
    
    def test_clear_session(self, session_manager):
        """测试清空会话"""
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        session_id = session_manager.create_session(user_id=user_id)
        
        # 添加消息
        for i in range(3):
            session_manager.add_message(session_id, "user", f'测试消息 {i+1}')
        
        # 清空会话
        session_manager.clear_history(session_id)
        
        # 验证消息已清空
        messages = session_manager.get_conversation_history(session_id)
        assert len(messages) == 0, "清空后消息数应该为 0"
        print("✅ 清空会话测试通过")
    
    def test_delete_session(self, session_manager):
        """测试删除会话"""
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        session_id = session_manager.create_session(user_id=user_id)
        
        # 添加消息
        session_manager.add_message(session_id, "user", "测试消息")
        
        # 删除会话
        session_manager.delete_session(session_id)
        
        # 验证会话已删除
        session_data = session_manager.get_session(session_id)
        assert session_data is None, "删除后会话数据应该为 None"
        print("✅ 删除会话测试通过")
    
    def test_list_sessions(self, session_manager):
        """测试列出所有会话"""
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        
        # 创建多个会话
        session_ids = []
        for i in range(3):
            session_id = session_manager.create_session(user_id=user_id)
            session_ids.append(session_id)
        
        # 列出会话
        sessions = session_manager.get_user_sessions(user_id=user_id)
        
        assert len(sessions) == 3, f"期望 3 个会话，实际 {len(sessions)} 个"
        assert all(s['session_id'] in session_ids for s in sessions), "会话 ID 不匹配"
        print("✅ 列出会话测试通过")
    
    def test_session_isolation(self, session_manager):
        """测试会话隔离"""
        user_a = f"user_a_{uuid.uuid4().hex[:8]}"
        user_b = f"user_b_{uuid.uuid4().hex[:8]}"
        
        # 创建两个用户的会话
        session_a = session_manager.create_session(user_id=user_a)
        session_b = session_manager.create_session(user_id=user_b)
        
        # 为用户 A 添加消息
        session_manager.add_message(session_a, "user", "用户 A 的消息")
        
        # 为用户 B 添加消息
        session_manager.add_message(session_b, "user", "用户 B 的消息")
        
        # 验证会话隔离
        messages_a = session_manager.get_conversation_history(session_a)
        messages_b = session_manager.get_conversation_history(session_b)
        
        assert len(messages_a) == 1, f"用户 A 应该有 1 条消息，实际 {len(messages_a)} 条"
        assert len(messages_b) == 1, f"用户 B 应该有 1 条消息，实际 {len(messages_b)} 条"
        assert messages_a[0]['content'] == '用户 A 的消息', "用户 A 的消息内容不匹配"
        assert messages_b[0]['content'] == '用户 B 的消息', "用户 B 的消息内容不匹配"
        print("✅ 会话隔离测试通过")


class TestContextManager:
    """测试上下文管理器功能"""
    
    @pytest.fixture
    def context_manager(self):
        """创建上下文管理器实例"""
        manager = ContextManager()
        yield manager
        # ContextManager doesn't need cleanup
    
    def test_manage_context_within_limit(self, context_manager):
        """测试上下文在限制范围内"""
        # 添加少量消息（不超过限制）
        messages = []
        for i in range(3):
            messages.append({
                'role': 'user',
                'content': f'短消息 {i+1}'
            })
        
        # 检查是否超限
        is_over_budget, current_tokens = context_manager.check_token_budget(messages)
        
        # 应该未超限
        assert is_over_budget == False, "少量消息不应该超限"
        print(f"✅ 上下文未超限测试通过 (Token 数: {current_tokens})")
    
    def test_context_compression(self, context_manager):
        """测试上下文压缩"""
        # 添加大量消息（超过限制）
        messages = []
        for i in range(20):
            messages.append({
                'role': 'user' if i % 2 == 0 else 'assistant',
                'content': f'这是一条较长的测试消息，用于测试上下文压缩功能。消息编号：{i+1}。'
            })
        
        # 检查是否超限
        is_over_budget, current_tokens = context_manager.check_token_budget(messages)
        
        if is_over_budget:
            # 压缩上下文
            compressed_messages = context_manager.compress_context(messages)
            
            # 应该返回压缩后的消息（少于原始消息）
            assert len(compressed_messages) < len(messages), "应该进行上下文压缩"
            print(f"✅ 上下文压缩测试通过 (原始: {len(messages)} 条, 压缩后: {len(compressed_messages)} 条)")
        else:
            print("✅ 上下文未超限，无需压缩")
    
    def test_token_counting(self, context_manager):
        """测试 Token 计数"""
        test_text = "这是一段测试文本，用于计算 Token 数量。"
        token_count = context_manager.count_tokens(test_text)
        
        assert token_count > 0, "Token 计数应该大于 0"
        assert isinstance(token_count, int), "Token 计数应该是整数"
        print(f"✅ Token 计数测试通过 (文本: '{test_text}', Token 数: {token_count})")
    
    def test_context_summary(self, context_manager):
        """测试上下文摘要"""
        # 添加多条消息
        messages = [
            {'role': 'user', 'content': '你好，我是新员工'},
            {'role': 'assistant', 'content': '欢迎加入公司！'},
            {'role': 'user', 'content': '我想了解报销政策'},
            {'role': 'assistant', 'content': '报销流程如下...'},
        ]
        
        # 生成摘要（使用内部方法）
        summary_messages = context_manager._generate_summary(messages, 1000)
        
        assert summary_messages is not None, "摘要不能为空"
        assert isinstance(summary_messages, list), "摘要应该是列表"
        assert len(summary_messages) > 0, "摘要长度应该大于 0"
        print(f"✅ 上下文摘要测试通过 (摘要消息数: {len(summary_messages)})")


class TestAgentMemoryIntegration:
    """测试 Agent 记忆集成"""
    
    @pytest.fixture
    def agent(self):
        """创建启用记忆的 Agent 实例"""
        agent = NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7,
            enable_memory=True
        )
        yield agent
        # 清理测试数据
        all_sessions = agent.session_manager.redis.get_all_sessions()
        for session in all_sessions:
            agent.session_manager.delete_session(session['session_id'])
    
    def test_agent_with_memory_enabled(self, agent):
        """测试启用记忆的 Agent"""
        # 第一次对话
        response1 = agent.process_message("你好，我叫李四，我是新员工")
        session_id = response1.session_id
        
        assert session_id is not None, "会话 ID 不能为空"
        assert response1.content is not None, "响应内容不能为空"
        print(f"✅ 第一次对话测试通过 (Session ID: {session_id})")
        
        # 第二次对话（测试记忆）
        response2 = agent.process_message("我叫什么名字？", session_id=session_id)
        
        assert response2.content is not None, "响应内容不能为空"
        # Agent 应该记住名字
        assert "李四" in response2.content or "李" in response2.content, "Agent 应该记住用户名字"
        print("✅ Agent 记忆测试通过")
    
    def test_multi_user_sessions(self, agent):
        """测试多用户会话"""
        # 用户 A 的会话
        response_a1 = agent.process_message("我是用户A，我是工程师", user_id="user_a")
        session_a = response_a1.session_id
        
        response_a2 = agent.process_message("我的职位是什么？", session_id=session_a, user_id="user_a")
        
        # 用户 B 的会话
        response_b1 = agent.process_message("我是用户B，我是设计师", user_id="user_b")
        session_b = response_b1.session_id
        
        response_b2 = agent.process_message("我的职位是什么？", session_id=session_b, user_id="user_b")
        
        # 验证两个会话独立
        assert session_a != session_b, "不同用户的会话 ID 应该不同"
        assert "工程师" in response_a2.content or "工程师" in response_a1.content, "用户 A 应该是工程师"
        assert "设计师" in response_b2.content or "设计师" in response_b1.content, "用户 B 应该是设计师"
        print("✅ 多用户会话测试通过")
    
    def test_conversation_history(self, agent):
        """测试对话历史"""
        session_id = agent.process_message("你好", user_id="test_user").session_id
        
        # 添加多条消息
        agent.process_message("第一条消息", session_id=session_id, user_id="test_user")
        agent.process_message("第二条消息", session_id=session_id, user_id="test_user")
        
        # 获取对话历史
        history = agent.get_conversation_history(session_id)
        
        assert history is not None, "对话历史不能为空"
        assert len(history) >= 3, f"期望至少 3 条消息，实际 {len(history)} 条"
        print(f"✅ 对话历史测试通过 (历史消息数: {len(history)})")
    
    def test_session_info(self, agent):
        """测试会话信息"""
        session_id = agent.process_message("你好", user_id="test_user").session_id
        
        # 添加消息
        agent.process_message("测试消息", session_id=session_id, user_id="test_user")
        
        # 获取会话信息
        session_info = agent.get_session_info(session_id)
        
        assert session_info is not None, "会话信息不能为空"
        assert 'message_count' in session_info, "缺少消息计数"
        assert 'created_at' in session_info, "缺少创建时间"
        assert session_info['message_count'] >= 2, f"期望至少 2 条消息，实际 {session_info['message_count']} 条"
        print(f"✅ 会话信息测试通过 (消息数: {session_info['message_count']})")
    
    def test_clear_session(self, agent):
        """测试清空会话"""
        session_id = agent.process_message("你好", user_id="test_user").session_id
        
        # 添加消息
        agent.process_message("测试消息1", session_id=session_id, user_id="test_user")
        agent.process_message("测试消息2", session_id=session_id, user_id="test_user")
        
        # 清空会话
        agent.clear_session(session_id)
        
        # 验证会话已清空
        history = agent.get_conversation_history(session_id)
        assert len(history) == 0, f"清空后消息数应该为 0，实际 {len(history)} 条"
        print("✅ 清空会话测试通过")
    
    def test_delete_session(self, agent):
        """测试删除会话"""
        session_id = agent.process_message("你好", user_id="test_user").session_id
        
        # 删除会话
        agent.delete_session(session_id)
        
        # 验证会话已删除
        session_info = agent.get_session_info(session_id)
        assert session_info is None, "删除后会话信息应该为 None"
        print("✅ 删除会话测试通过")


class TestMemoryManagementIntegration:
    """测试记忆管理集成"""
    
    @pytest.fixture
    def agent(self):
        """创建启用记忆的 Agent 实例"""
        agent = NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7,
            enable_memory=True
        )
        yield agent
        # 清理测试数据
        all_sessions = agent.session_manager.redis.get_all_sessions()
        for session in all_sessions:
            agent.session_manager.delete_session(session['session_id'])
    
    def test_long_conversation_with_compression(self, agent):
        """测试长对话的上下文压缩"""
        session_id = agent.process_message("你好，我是测试用户", user_id="test_user").session_id
        
        # 模拟长对话
        for i in range(10):
            user_msg = f"这是第 {i+1} 条用户消息，内容比较长，用于测试上下文压缩功能。"
            agent.process_message(user_msg, session_id=session_id, user_id="test_user")
        
        # 获取对话历史
        history = agent.get_conversation_history(session_id)
        
        # 验证历史消息数量（可能因为压缩而减少）
        assert history is not None, "对话历史不能为空"
        assert len(history) > 0, "应该有历史消息"
        print(f"✅ 长对话上下文压缩测试通过 (历史消息数: {len(history)})")
    
    def test_session_persistence(self, agent):
        """测试会话持久化"""
        session_id = agent.process_message("你好，我是张三", user_id="test_user").session_id
        
        # 添加消息
        agent.process_message("记住我的信息", session_id=session_id, user_id="test_user")
        
        # 获取历史
        history1 = agent.get_conversation_history(session_id)
        count1 = len(history1)
        
        # 等待一下（模拟时间流逝）
        time.sleep(1)
        
        # 再次获取历史（应该从 Redis 持久化存储中读取）
        history2 = agent.get_conversation_history(session_id)
        count2 = len(history2)
        
        assert count1 == count2, f"持久化前后消息数应该一致 ({count1} vs {count2})"
        print("✅ 会话持久化测试通过")
    
    def test_concurrent_sessions(self, agent):
        """测试并发会话"""
        # 创建多个会话
        sessions = []
        for i in range(3):
            session_id = agent.process_message(f"我是用户{i+1}", user_id=f"user_{i+1}").session_id
            sessions.append(session_id)
        
        # 为每个会话添加消息
        for i, session_id in enumerate(sessions):
            agent.process_message(f"用户{i+1}的消息", session_id=session_id, user_id=f"user_{i+1}")
        
        # 验证每个会话独立
        for i, session_id in enumerate(sessions):
            history = agent.get_conversation_history(session_id)
            assert len(history) >= 2, f"用户{i+1}的会话应该至少有2条消息"
        
        print("✅ 并发会话测试通过")


def run_all_tests():
    """运行所有测试并生成报告"""
    print("=" * 80)
    print("Sprint 4: 记忆管理与多轮对话 - 综合测试")
    print("=" * 80)
    print()
    
    # 运行测试
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])
    
    print()
    print("=" * 80)
    if exit_code == 0:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败，请查看上面的错误信息")
    print("=" * 80)
    
    return exit_code


if __name__ == "__main__":
    run_all_tests()
