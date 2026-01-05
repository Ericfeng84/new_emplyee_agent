"""
集成测试 - 工具调用功能
Sprint 3: Tool Calling 集成测试
"""

import pytest
from nexus_agent.agent.agent import NexusLangChainAgent
from nexus_agent.config.settings import config


class TestToolCallingIntegration:
    """测试工具调用集成"""
    
    @pytest.fixture
    def agent(self):
        """创建测试用的 agent"""
        return NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7
        )
    
    def test_employee_search_tool_calling(self, agent):
        """测试员工搜索工具调用"""
        response = agent.process_message("张三的电话是多少？")
        
        assert response.success is True
        assert "张三" in response.content
        # 检查是否使用了工具
        assert response.tool_calls is not None
        assert len(response.tool_calls) > 0
    
    def test_meeting_room_booking_tool_calling(self, agent):
        """测试会议室预订工具调用"""
        response = agent.process_message(
            "帮我预订 A1 会议室，明天下午2点，开1小时会，我是张三，会议目的是项目讨论"
        )
        
        assert response.success is True
        assert "成功预订" in response.content or "预订失败" in response.content
        assert response.tool_calls is not None
    
    def test_leave_balance_query_tool_calling(self, agent):
        """测试假期余额查询工具调用"""
        response = agent.process_message("查一下张三的假期余额")
        
        assert response.success is True
        assert "年假" in response.content or "未找到" in response.content
        assert response.tool_calls is not None
    
    def test_multi_tool_calling(self, agent):
        """测试多工具调用"""
        # 先查可用会议室
        response1 = agent.process_message(
            "明天下午2点有哪些会议室可用？"
        )
        
        # 再预订会议室
        response2 = agent.process_message(
            "帮我预订 A1 会议室，明天下午2点，开1小时会，我是张三"
        )
        
        assert response1.success is True
        assert response2.success is True
    
    def test_no_tool_needed(self, agent):
        """测试不需要工具的情况"""
        response = agent.process_message("你好")
        
        assert response.success is True
        # 普通问候不需要工具调用
        assert response.tool_calls is None or len(response.tool_calls) == 0
    
    def test_tool_with_missing_params(self, agent):
        """测试缺少参数时的处理"""
        response = agent.process_message("帮我预订会议室")
        
        assert response.success is True
        # Agent 应该询问缺少的参数
        assert "日期" in response.content or "时间" in response.content or "会议室" in response.content


class TestToolSelectionAccuracy:
    """测试工具选择准确性"""
    
    @pytest.fixture
    def agent(self):
        return NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7
        )
    
    def test_selects_search_employee_tool(self, agent):
        """测试选择员工搜索工具"""
        test_cases = [
            "张三的电话",
            "技术部有哪些人",
            "找一下李四",
        ]
        
        for query in test_cases:
            response = agent.process_message(query)
            # 应该调用了 search_employee_directory 工具
            assert response.success is True
            assert "张三" in response.content or "李四" in response.content or "技术部" in response.content
    
    def test_selects_book_meeting_room_tool(self, agent):
        """测试选择预订会议室工具"""
        test_cases = [
            "帮我订个会议室",
            "预订 A1 会议室",
            "明天下午2点开个会",
        ]
        
        for query in test_cases:
            response = agent.process_message(query)
            assert response.success is True
            # 应该询问参数或尝试预订
    
    def test_selects_query_leave_balance_tool(self, agent):
        """测试选择假期查询工具"""
        test_cases = [
            "我还有多少天年假",
            "查一下张三的假期",
            "我的假期余额",
        ]
        
        for query in test_cases:
            response = agent.process_message(query)
            assert response.success is True
            assert "年假" in response.content or "病假" in response.content or "未找到" in response.content
    
    def test_selects_get_available_rooms_tool(self, agent):
        """测试选择查询可用会议室工具"""
        test_cases = [
            "明天下午有哪些会议室可用",
            "查一下明天上午的会议室",
            "2026-01-10 下午2点有会议室吗",
        ]
        
        for query in test_cases:
            response = agent.process_message(query)
            assert response.success is True
            # 应该返回会议室信息或询问时间


class TestToolErrorHandling:
    """测试工具错误处理"""
    
    @pytest.fixture
    def agent(self):
        return NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7
        )
    
    def test_invalid_employee_search(self, agent):
        """测试搜索不存在的员工"""
        response = agent.process_message("查找不存在的人的信息")
        
        assert response.success is True
        assert "未找到" in response.content
    
    def test_invalid_meeting_room(self, agent):
        """测试预订不存在的会议室"""
        response = agent.process_message(
            "预订 XYZ 会议室，明天下午2点，开1小时会，我是张三"
        )
        
        assert response.success is True
        # 应该返回错误或询问会议室名称
    
    def test_invalid_date_format(self, agent):
        """测试无效的日期格式"""
        response = agent.process_message(
            "预订 A1 会议室，明天下午2点，开1小时会，我是张三"
        )
        
        assert response.success is True
        # Agent 应该询问具体日期


class TestToolPerformance:
    """测试工具性能"""
    
    @pytest.fixture
    def agent(self):
        return NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7
        )
    
    def test_tool_response_time(self, agent):
        """测试工具响应时间"""
        import time
        
        start_time = time.time()
        response = agent.process_message("张三的电话是多少？")
        end_time = time.time()
        
        assert response.success is True
        # 响应时间应该在合理范围内（< 30秒）
        assert (end_time - start_time) < 30.0
    
    def test_multiple_tool_calls_performance(self, agent):
        """测试多次工具调用的性能"""
        queries = [
            "张三的电话是多少？",
            "查一下李四的假期余额",
            "明天下午2点有哪些会议室可用？",
        ]
        
        import time
        start_time = time.time()
        
        for query in queries:
            response = agent.process_message(query)
            assert response.success is True
        
        end_time = time.time()
        
        # 总响应时间应该在合理范围内（< 90秒）
        assert (end_time - start_time) < 90.0


class TestToolContextIntegration:
    """测试工具与上下文的集成"""
    
    @pytest.fixture
    def agent(self):
        return NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7
        )
    
    def test_tool_result_in_conversation(self, agent):
        """测试工具结果在对话中的使用"""
        # 第一轮：查询员工信息
        response1 = agent.process_message("张三的电话是多少？")
        
        # 第二轮：基于之前的信息
        response2 = agent.process_message("他在哪个部门？")
        
        assert response1.success is True
        assert response2.success is True
        # 第二轮应该能够理解"他"指的是张三
        assert "技术部" in response2.content or "张三" in response2.content
    
    def test_sequential_tool_calls(self, agent):
        """测试连续工具调用"""
        # 先查询可用会议室
        response1 = agent.process_message(
            "明天下午2点有哪些会议室可用？"
        )
        
        # 然后预订会议室
        response2 = agent.process_message(
            "帮我预订 A1 会议室，明天下午2点，开1小时会，我是张三"
        )
        
        assert response1.success is True
        assert response2.success is True
        # 第二次调用应该成功预订
        assert "成功预订" in response2.content or "预订失败" in response2.content


class TestToolMetadata:
    """测试工具元数据"""
    
    @pytest.fixture
    def agent(self):
        return NexusLangChainAgent(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7
        )
    
    def test_response_metadata(self, agent):
        """测试响应元数据"""
        response = agent.process_message("张三的电话是多少？")
        
        assert response.success is True
        assert response.duration is not None
        assert response.context_id is not None
        assert response.metadata is not None
        assert "provider" in response.metadata
        assert "model" in response.metadata
    
    def test_tool_calls_metadata(self, agent):
        """测试工具调用元数据"""
        response = agent.process_message("张三的电话是多少？")
        
        assert response.success is True
        if response.tool_calls:
            # 检查工具调用结构
            for tool_call in response.tool_calls:
                assert "name" in tool_call
