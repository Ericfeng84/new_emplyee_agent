"""
单元测试 - API 工具函数
Sprint 3: Tool Calling 功能测试
"""

import pytest
from nexus_agent.agent.api_tools import (
    search_employee_directory,
    book_meeting_room,
    query_leave_balance,
    get_available_meeting_rooms
)
from nexus_agent.data.mock_data import (
    employee_directory,
    meeting_room_system,
    leave_system
)


class TestSearchEmployeeDirectory:
    """测试员工目录搜索工具"""
    
    def test_search_by_name(self):
        """测试按姓名搜索"""
        result = search_employee_directory.invoke({"query": "张三"})
        assert "张三" in result
        assert "技术部" in result
        assert "zhangsan@company.com" in result
        assert "内线 1001" in result
    
    def test_search_by_department(self):
        """测试按部门搜索"""
        result = search_employee_directory.invoke({"query": "技术部"})
        assert "张三" in result
        assert "技术部" in result
    
    def test_search_by_position(self):
        """测试按职位搜索"""
        result = search_employee_directory.invoke({"query": "产品经理"})
        assert "李四" in result
        assert "市场部" in result
    
    def test_not_found(self):
        """测试未找到的情况"""
        result = search_employee_directory.invoke({"query": "不存在的人"})
        assert "未找到" in result
        assert "不存在的人" in result
    
    def test_partial_match(self):
        """测试部分匹配"""
        result = search_employee_directory.invoke({"query": "张"})
        assert "张三" in result


class TestBookMeetingRoom:
    """测试会议室预订工具"""
    
    def test_successful_booking(self):
        """测试成功预订"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        result = book_meeting_room.invoke({
            "room_name": "A1",
            "date": "2026-01-10",
            "time": "14:00",
            "duration": 60,
            "booker": "张三",
            "purpose": "项目讨论"
        })
        assert "成功预订" in result
        assert "A1会议室" in result
        assert "2026-01-10" in result
        assert "14:00" in result
        assert "张三" in result
    
    def test_duplicate_booking(self):
        """测试重复预订"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        # 第一次预订
        book_meeting_room.invoke({
            "room_name": "A1",
            "date": "2026-01-11",
            "time": "14:00",
            "duration": 60,
            "booker": "张三",
            "purpose": "项目讨论"
        })
        
        # 第二次预订同一时间
        result = book_meeting_room.invoke({
            "room_name": "A1",
            "date": "2026-01-11",
            "time": "14:00",
            "duration": 60,
            "booker": "李四",
            "purpose": "其他会议"
        })
        assert "已被预订" in result
        assert "预订失败" in result
    
    def test_invalid_room(self):
        """测试无效会议室"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        result = book_meeting_room.invoke({
            "room_name": "INVALID",
            "date": "2026-01-10",
            "time": "14:00",
            "duration": 60,
            "booker": "张三",
            "purpose": "项目讨论"
        })
        assert "预订失败" in result
    
    def test_booking_details(self):
        """测试预订详情完整性"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        result = book_meeting_room.invoke({
            "room_name": "B2",
            "date": "2026-01-15",
            "time": "10:00",
            "duration": 90,
            "booker": "李四",
            "purpose": "周会"
        })
        assert "预订号" in result
        assert "90 分钟" in result
        assert "周会" in result


class TestQueryLeaveBalance:
    """测试假期余额查询工具"""
    
    def test_query_existing_employee(self):
        """测试查询存在的员工"""
        result = query_leave_balance.invoke({"employee_name": "张三"})
        assert "张三 的假期余额" in result
        assert "年假：15 天" in result
        assert "病假：10 天" in result
        assert "事假：3 天" in result
        assert "已用" in result
    
    def test_query_nonexistent_employee(self):
        """测试查询不存在的员工"""
        result = query_leave_balance.invoke({"employee_name": "不存在的人"})
        assert "未找到" in result
        assert "不存在的人" in result
    
    def test_leave_balance_format(self):
        """测试假期余额格式"""
        result = query_leave_balance.invoke({"employee_name": "李四"})
        assert "📅" in result or "年假" in result
        assert "🤒" in result or "病假" in result
        assert "📝" in result or "事假" in result


class TestGetAvailableMeetingRooms:
    """测试获取可用会议室工具"""
    
    def test_get_available_rooms(self):
        """测试获取可用会议室"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        result = get_available_meeting_rooms.invoke({
            "date": "2026-01-10",
            "time": "14:00"
        })
        assert "可用会议室列表" in result
        assert "A1会议室" in result or "A2会议室" in result
    
    def test_with_capacity_filter(self):
        """测试带容量过滤"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        result = get_available_meeting_rooms.invoke({
            "date": "2026-01-10",
            "time": "14:00",
            "min_capacity": 20
        })
        # 应该只返回容量 >= 20 的会议室
        assert "C1会议室" in result  # 容量 30
        assert "A2会议室" in result  # 容量 20
    
    def test_no_available_rooms(self):
        """测试没有可用会议室的情况"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        # 先预订所有会议室
        for room in ["A1", "A2", "B1", "B2", "C1"]:
            book_meeting_room.invoke({
                "room_name": room,
                "date": "2026-01-20",
                "time": "09:00",
                "duration": 60,
                "booker": "测试",
                "purpose": "测试"
            })
        
        result = get_available_meeting_rooms.invoke({
            "date": "2026-01-20",
            "time": "09:00"
        })
        assert "没有可用的会议室" in result
    
    def test_room_details(self):
        """测试会议室详情"""
        # Reset bookings before test
        meeting_room_system.reset()
        
        result = get_available_meeting_rooms.invoke({
            "date": "2026-01-10",
            "time": "15:00"
        })
        # 检查是否包含设备信息
        assert "投影仪" in result or "白板" in result or "视频会议" in result


class TestMockDataSystems:
    """测试模拟数据系统"""
    
    def test_employee_directory_search(self):
        """测试员工目录搜索"""
        results = employee_directory.search("张")
        assert len(results) > 0
        assert any(emp["name"] == "张三" for emp in results)
    
    def test_employee_directory_structure(self):
        """测试员工数据结构"""
        result = employee_directory.search("张三")
        assert len(result) == 1
        emp = result[0]
        assert "name" in emp
        assert "department" in emp
        assert "position" in emp
        assert "email" in emp
        assert "phone" in emp
        assert "location" in emp
        assert "manager" in emp
    
    def test_meeting_room_availability(self):
        """测试会议室可用性检查"""
        # Reset bookings before test
        meeting_room_system.reset()
        assert meeting_room_system.check_availability("A1", "2026-01-10", "14:00") == True
    
    def test_meeting_room_booking(self):
        """测试会议室预订"""
        result = meeting_room_system.book_room(
            room_name="A1",
            date="2026-01-10",
            time="16:00",
            duration=60,
            booker="张三",
            purpose="测试"
        )
        assert result["success"] == True
        assert "booking_id" in result["booking"]
    
    def test_meeting_room_availability_after_booking(self):
        """测试预订后的可用性"""
        # 预订会议室
        meeting_room_system.book_room(
            room_name="B1",
            date="2026-01-10",
            time="17:00",
            duration=60,
            booker="李四",
            purpose="测试"
        )
        
        # 检查同一时间是否可用
        assert meeting_room_system.check_availability("B1", "2026-01-10", "17:00") == False
    
    def test_leave_system_query(self):
        """测试假期系统查询"""
        balance = leave_system.query_balance("张三")
        assert balance is not None
        assert balance["annual"] == 15
        assert balance["sick"] == 10
        assert balance["personal"] == 3
    
    def test_leave_system_format(self):
        """测试假期信息格式化"""
        info = leave_system.format_balance_info("王五")
        assert "王五" in info
        assert "年假" in info
        assert "病假" in info
        assert "事假" in info
    
    def test_leave_system_nonexistent(self):
        """测试查询不存在的员工"""
        balance = leave_system.query_balance("不存在")
        assert balance is None


class TestToolIntegration:
    """测试工具集成"""
    
    def test_tool_has_name(self):
        """测试工具有名称属性"""
        assert hasattr(search_employee_directory, 'name')
        assert hasattr(book_meeting_room, 'name')
        assert hasattr(query_leave_balance, 'name')
        assert hasattr(get_available_meeting_rooms, 'name')
    
    def test_tool_has_description(self):
        """测试工具有描述属性"""
        assert hasattr(search_employee_directory, 'description')
        assert hasattr(book_meeting_room, 'description')
        assert hasattr(query_leave_balance, 'description')
        assert hasattr(get_available_meeting_rooms, 'description')
    
    def test_tool_returns_string(self):
        """测试工具返回字符串"""
        result1 = search_employee_directory.invoke({"query": "张三"})
        assert isinstance(result1, str)
        
        result2 = book_meeting_room.invoke({
            "room_name": "A1",
            "date": "2026-01-10",
            "time": "18:00",
            "duration": 60,
            "booker": "张三",
            "purpose": "测试"
        })
        assert isinstance(result2, str)
        
        result3 = query_leave_balance.invoke({"employee_name": "张三"})
        assert isinstance(result3, str)
        
        result4 = get_available_meeting_rooms.invoke({
            "date": "2026-01-10",
            "time": "19:00"
        })
        assert isinstance(result4, str)
