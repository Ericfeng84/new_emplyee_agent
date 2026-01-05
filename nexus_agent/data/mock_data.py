"""
模拟数据存储
用于支持 Sprint 3 的工具调用功能
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


class MockEmployeeDirectory:
    """模拟员工目录数据库"""
    
    def __init__(self):
        # 模拟员工数据
        self.employees = {
            "张三": {
                "name": "张三",
                "department": "技术部",
                "position": "高级工程师",
                "email": "zhangsan@company.com",
                "phone": "内线 1001",
                "location": "3楼 A区",
                "manager": "李经理"
            },
            "李四": {
                "name": "李四",
                "department": "市场部",
                "position": "产品经理",
                "email": "lisi@company.com",
                "phone": "内线 2001",
                "location": "4楼 B区",
                "manager": "王总监"
            },
            "王五": {
                "name": "王五",
                "department": "人力资源部",
                "position": "HR 专员",
                "email": "wangwu@company.com",
                "phone": "内线 3001",
                "location": "5楼 C区",
                "manager": "陈总监"
            },
            "赵六": {
                "name": "赵六",
                "department": "财务部",
                "position": "会计师",
                "email": "zhaoliu@company.com",
                "phone": "内线 4001",
                "location": "4楼 D区",
                "manager": "周经理"
            }
        }
    
    def search(self, query: str) -> List[Dict]:
        """
        搜索员工信息
        
        Args:
            query: 搜索关键词（姓名、部门、职位等）
            
        Returns:
            匹配的员工列表
        """
        results = []
        query_lower = query.lower()
        
        for emp_id, emp_data in self.employees.items():
            # 搜索姓名
            if query_lower in emp_data["name"].lower():
                results.append(emp_data)
                continue
            
            # 搜索部门
            if query_lower in emp_data["department"].lower():
                results.append(emp_data)
                continue
            
            # 搜索职位
            if query_lower in emp_data["position"].lower():
                results.append(emp_data)
        
        return results


class MockMeetingRoomSystem:
    """模拟会议室预订系统"""
    
    def __init__(self):
        # 模拟会议室
        self.rooms = {
            "A1": {"name": "A1会议室", "capacity": 10, "floor": "3楼", "equipment": ["投影仪", "白板"]},
            "A2": {"name": "A2会议室", "capacity": 20, "floor": "3楼", "equipment": ["投影仪", "白板", "视频会议"]},
            "B1": {"name": "B1会议室", "capacity": 8, "floor": "4楼", "equipment": ["白板"]},
            "B2": {"name": "B2会议室", "capacity": 15, "floor": "4楼", "equipment": ["投影仪", "白板"]},
            "C1": {"name": "C1会议室", "capacity": 30, "floor": "5楼", "equipment": ["投影仪", "音响", "视频会议"]},
        }
        
        # 模拟预订记录
        self.bookings = []
    
    def reset(self):
        """重置预订记录"""
        self.bookings = []
    
    def check_availability(self, room_name: str, date: str, time: str) -> bool:
        """
        检查会议室是否可用
        
        Args:
            room_name: 会议室名称
            date: 日期 (YYYY-MM-DD)
            time: 时间 (HH:MM)
            
        Returns:
            是否可用
        """
        # 检查会议室是否存在
        if room_name not in self.rooms:
            return False
        
        # 检查是否已被预订
        for booking in self.bookings:
            if (booking["room_name"] == room_name and 
                booking["date"] == date and 
                booking["time"] == time):
                return False
        
        return True
    
    def book_room(self, room_name: str, date: str, time: str, duration: int, 
                  booker: str, purpose: str) -> Dict:
        """
        预订会议室
        
        Args:
            room_name: 会议室名称
            date: 日期 (YYYY-MM-DD)
            time: 开始时间 (HH:MM)
            duration: 持续时间（分钟）
            booker: 预订人
            purpose: 会议目的
            
        Returns:
            预订结果
        """
        # 检查可用性
        if not self.check_availability(room_name, date, time):
            return {
                "success": False,
                "message": f"{room_name} 在 {date} {time} 已被预订"
            }
        
        # 创建预订
        booking = {
            "room_name": room_name,
            "date": date,
            "time": time,
            "duration": duration,
            "booker": booker,
            "purpose": purpose,
            "booking_id": f"BK{len(self.bookings) + 1:04d}",
            "created_at": datetime.now().isoformat()
        }
        
        self.bookings.append(booking)
        
        return {
            "success": True,
            "message": f"成功预订 {room_name}",
            "booking": booking
        }
    
    def get_available_rooms(self, date: str, time: str, capacity: int = None) -> List[Dict]:
        """
        获取可用会议室列表
        
        Args:
            date: 日期
            time: 时间
            capacity: 最小容量要求（可选）
            
        Returns:
            可用会议室列表
        """
        available = []
        
        for room_id, room_info in self.rooms.items():
            # 检查容量
            if capacity and room_info["capacity"] < capacity:
                continue
            
            # 检查可用性
            if self.check_availability(room_id, date, time):
                available.append({
                    "room_id": room_id,
                    **room_info
                })
        
        return available


class MockLeaveSystem:
    """模拟请假管理系统"""
    
    def __init__(self):
        # 模拟员工假期余额
        self.leave_balances = {
            "张三": {
                "annual": 15,  # 年假（天）
                "sick": 10,    # 病假（天）
                "personal": 3,   # 事假（天）
                "used_annual": 5,
                "used_sick": 2,
                "used_personal": 1
            },
            "李四": {
                "annual": 12,
                "sick": 10,
                "personal": 3,
                "used_annual": 8,
                "used_sick": 1,
                "used_personal": 0
            },
            "王五": {
                "annual": 10,
                "sick": 10,
                "personal": 3,
                "used_annual": 3,
                "used_sick": 0,
                "used_personal": 1
            }
        }
    
    def query_balance(self, employee_name: str) -> Optional[Dict]:
        """
        查询员工假期余额
        
        Args:
            employee_name: 员工姓名
            
        Returns:
            假期余额信息
        """
        return self.leave_balances.get(employee_name)
    
    def format_balance_info(self, employee_name: str) -> str:
        """
        格式化假期余额信息
        
        Args:
            employee_name: 员工姓名
            
        Returns:
            格式化的余额信息
        """
        balance = self.query_balance(employee_name)
        
        if not balance:
            return f"未找到员工 {employee_name} 的假期信息"
        
        info = f"""
【{employee_name} 的假期余额】

📅 年假：{balance['annual']} 天（已用 {balance['used_annual']} 天）
🤒 病假：{balance['sick']} 天（已用 {balance['used_sick']} 天）
📝 事假：{balance['personal']} 天（已用 {balance['used_personal']} 天）

💡 提示：请假需提前通过 HR 系统提交申请
        """.strip()
        
        return info


# 全局实例
employee_directory = MockEmployeeDirectory()
meeting_room_system = MockMeetingRoomSystem()
leave_system = MockLeaveSystem()
