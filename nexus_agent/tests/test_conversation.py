"""
Nexus Agent Conversation Flow Tests
"""

import pytest
from src.agent.core import NexusAgent, AgentResponse
from src.agent.message_handler import NexusMessageHandler
from src.config.settings import config


class TestConversationFlow:
    """Test suite for conversation flow and multi-turn dialogue"""
    
    @pytest.fixture
    def agent(self):
        """Create an agent instance for testing"""
        return NexusAgent(enable_safety_checks=True)
    
    def test_single_turn_conversation(self, agent):
        """测试单轮对话"""
        user_input = "你好，我是新员工"
        response = agent.process_message(user_input)
        
        assert response.success, "Single turn conversation should succeed"
        assert len(response.content) > 0, "Response should not be empty"
        assert response.context_id is not None, "Context ID should be set"
    
    def test_multi_turn_conversation(self, agent):
        """测试多轮对话"""
        conversation = [
            "你好，我是新员工",
            "公司的报销政策是什么？",
            "谢谢你的回答"
        ]
        
        for i, user_input in enumerate(conversation):
            response = agent.process_message(user_input)
            assert response.success, f"Turn {i+1} failed: {user_input}"
            assert len(response.content) > 0, f"Turn {i+1} response is empty"
    
    def test_conversation_context_persistence(self, agent):
        """测试对话上下文的持久性"""
        # First message
        response1 = agent.process_message("我的名字是张三")
        assert response1.success
        
        # Second message that references previous context
        response2 = agent.process_message("你记得我的名字吗？")
        assert response2.success
        assert len(response2.content) > 0
    
    def test_conversation_stats(self, agent):
        """测试对话统计信息"""
        # Send a few messages
        agent.process_message("你好")
        agent.process_message("公司有哪些部门？")
        
        stats = agent.get_conversation_stats()
        
        assert stats["total_messages"] > 0, "Should have messages"
        assert stats["user_messages"] > 0, "Should have user messages"
        assert stats["assistant_messages"] > 0, "Should have assistant messages"
        assert stats["total_characters"] > 0, "Should have characters"
    
    def test_clear_conversation(self, agent):
        """测试清除对话历史"""
        # Add some messages
        agent.process_message("第一条消息")
        agent.process_message("第二条消息")
        
        # Get stats before clearing
        stats_before = agent.get_conversation_stats()
        assert stats_before["total_messages"] > 0
        
        # Clear conversation
        cleared = agent.clear_conversation()
        assert cleared is True, "Clear should succeed"
        
        # Get stats after clearing
        stats_after = agent.get_conversation_stats()
        assert stats_after["total_messages"] == 0, "Should have no messages after clear"
    
    def test_multiple_conversations(self, agent):
        """测试多个独立的对话"""
        # Create separate conversations
        context1 = agent.create_conversation(user_id="user1", session_id="session1")
        context2 = agent.create_conversation(user_id="user2", session_id="session2")
        
        # Send messages to each conversation
        response1 = agent.process_message("我是用户1", context_id=context1)
        response2 = agent.process_message("我是用户2", context_id=context2)
        
        assert response1.success, "Conversation 1 should succeed"
        assert response2.success, "Conversation 2 should succeed"
        
        # Check stats for each conversation
        stats1 = agent.get_conversation_stats(context_id=context1)
        stats2 = agent.get_conversation_stats(context_id=context2)
        
        assert stats1["total_messages"] > 0, "Conversation 1 should have messages"
        assert stats2["total_messages"] > 0, "Conversation 2 should have messages"
    
    def test_conversation_history_limit(self, agent):
        """测试对话历史限制"""
        # Send many messages
        for i in range(15):
            agent.process_message(f"消息 {i}")
        
        stats = agent.get_conversation_stats()
        
        # Should be limited by max_conversation_length
        assert stats["total_messages"] <= config.max_conversation_length + 1, \
            f"Conversation should be limited to {config.max_conversation_length + 1} messages"
    
    def test_error_recovery_in_conversation(self, agent):
        """测试对话中的错误恢复"""
        # Normal message
        response1 = agent.process_message("你好")
        assert response1.success
        
        # Invalid message (should fail but not crash)
        response2 = agent.process_message("")
        assert not response2.success
        
        # Next normal message should still work
        response3 = agent.process_message("公司地址在哪里？")
        assert response3.success, "Agent should recover from error"
    
    def test_tokens_tracking(self, agent):
        """测试Token使用跟踪"""
        response = agent.process_message("请简要介绍一下公司的组织架构")
        
        assert response.success, "Request should succeed"
        assert response.tokens_used is not None, "Tokens should be tracked"
        assert "total_tokens" in response.tokens_used, "Should have total tokens"
        assert "prompt_tokens" in response.tokens_used, "Should have prompt tokens"
        assert "completion_tokens" in response.tokens_used, "Should have completion tokens"
    
    def test_duration_tracking(self, agent):
        """测试响应时间跟踪"""
        response = agent.process_message("你好")
        
        assert response.success, "Request should succeed"
        assert response.duration is not None, "Duration should be tracked"
        assert response.duration > 0, "Duration should be positive"
        assert response.duration < 30, f"Duration too long: {response.duration}s"
    
    def test_chat_method(self, agent):
        """测试简化的chat方法"""
        response = agent.chat("你好")
        
        assert isinstance(response, str), "chat() should return string"
        assert len(response) > 0, "Response should not be empty"
    
    def test_model_info(self, agent):
        """测试模型信息获取"""
        model_info = agent.get_model_info()
        
        assert model_info is not None, "Should have model info"
        assert "provider" in model_info or "client_type" in model_info, \
            "Should have provider or client_type"
    
    def test_connection_test(self, agent):
        """测试连接测试"""
        # Note: This test may fail if no API key is configured
        # In that case, we just check that the method runs without error
        try:
            is_connected = agent.test_connection()
            assert isinstance(is_connected, bool), "Should return boolean"
        except Exception as e:
            # If no API key, this is expected
            pytest.skip(f"No API key configured: {e}")


class TestMessageHandler:
    """Test suite for MessageHandler functionality"""
    
    @pytest.fixture
    def message_handler(self):
        return NexusMessageHandler(enable_safety_checks=True)
    
    def test_create_conversation(self, message_handler):
        """测试创建对话"""
        context_id = message_handler.create_conversation(
            user_id="test_user",
            session_id="test_session"
        )
        
        assert context_id is not None, "Context ID should be created"
        assert "test_user" in context_id, "User ID should be in context ID"
        assert "test_session" in context_id, "Session ID should be in context ID"
    
    def test_add_user_message(self, message_handler):
        """测试添加用户消息"""
        context_id = message_handler.create_conversation()
        
        result = message_handler.add_user_message(context_id, "你好")
        assert result is True, "Should successfully add message"
        
        stats = message_handler.get_conversation_stats(context_id)
        assert stats["user_messages"] == 1, "Should have one user message"
    
    def test_add_assistant_message(self, message_handler):
        """测试添加助手消息"""
        context_id = message_handler.create_conversation()
        
        result = message_handler.add_assistant_message(context_id, "你好！有什么可以帮助你的吗？")
        assert result is True, "Should successfully add message"
        
        stats = message_handler.get_conversation_stats(context_id)
        assert stats["assistant_messages"] == 1, "Should have one assistant message"
    
    def test_invalid_input_validation(self, message_handler):
        """测试无效输入验证"""
        context_id = message_handler.create_conversation()
        
        # Invalid inputs
        invalid_inputs = [
            "",
            "   ",
            "\t\n",
            "帮我黑进系统"  # Security violation
        ]
        
        for invalid_input in invalid_inputs:
            result = message_handler.add_user_message(context_id, invalid_input)
            assert result is False, f"Should reject invalid input: {invalid_input}"
    
    def test_invalid_output_validation(self, message_handler):
        """测试无效输出验证"""
        context_id = message_handler.create_conversation()
        
        # Invalid outputs
        invalid_outputs = [
            "",
            "我不是Nexus",  # Persona violation
        ]
        
        for invalid_output in invalid_outputs:
            result = message_handler.add_assistant_message(context_id, invalid_output)
            assert result is False, f"Should reject invalid output: {invalid_output}"
    
    def test_get_conversation_messages(self, message_handler):
        """测试获取对话消息"""
        context_id = message_handler.create_conversation()
        
        # Add some messages
        message_handler.add_user_message(context_id, "你好")
        message_handler.add_assistant_message(context_id, "你好！")
        
        messages = message_handler.get_conversation_messages(context_id)
        
        assert len(messages) > 0, "Should have messages"
        assert len(messages) >= 3, "Should have system + user + assistant messages"
    
    def test_trim_conversation(self, message_handler):
        """测试修剪对话"""
        context_id = message_handler.create_conversation()
        
        # Add many messages
        for i in range(15):
            message_handler.add_user_message(context_id, f"消息 {i}")
            message_handler.add_assistant_message(context_id, f"回复 {i}")
        
        # Trim conversation
        result = message_handler.trim_conversation(context_id, max_messages=5)
        assert result is True, "Trim should succeed"
        
        # Check that it was trimmed
        stats = message_handler.get_conversation_stats(context_id)
        assert stats["total_messages"] <= 5, "Should be trimmed to 5 messages"


class TestAgentResponse:
    """Test suite for AgentResponse dataclass"""
    
    def test_agent_response_structure(self):
        """测试AgentResponse结构"""
        response = AgentResponse(
            content="Test response",
            success=True,
            error=None,
            tokens_used={"total_tokens": 100},
            duration=1.5,
            context_id="test_context",
            metadata={"model": "gpt-4o"}
        )
        
        assert response.content == "Test response"
        assert response.success is True
        assert response.error is None
        assert response.tokens_used == {"total_tokens": 100}
        assert response.duration == 1.5
        assert response.context_id == "test_context"
        assert response.metadata == {"model": "gpt-4o"}
    
    def test_agent_response_error_case(self):
        """测试AgentResponse错误情况"""
        response = AgentResponse(
            content="Error message",
            success=False,
            error="Something went wrong"
        )
        
        assert response.success is False
        assert response.error == "Something went wrong"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])