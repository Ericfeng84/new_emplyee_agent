"""
API 工具函数 - Sprint 3
模拟企业系统 API 调用：查人、订房、查假
"""

from langchain.tools import tool
from typing import Dict, List, Optional
from ..data.mock_data import employee_directory, meeting_room_system, leave_system


@tool
def search_employee_directory(query: str) -> str:
    """
    搜索员工目录，查找同事的联系方式和部门信息。
    
    Args:
        query: 搜索关键词，可以是姓名、部门或职位
    
    Returns:
        匹配的员工信息列表
    """
    results = employee_directory.search(query)
    
    if not results:
        return f"未找到与 '{query}' 相关的员工信息。请尝试其他关键词。"
    
    # 格式化结果
    output_parts = []
    for emp in results:
        emp_info = f"""
【{emp['name']}】
- 部门：{emp['department']}
- 职位：{emp['position']}
- 邮箱：{emp['email']}
- 电话：{emp['phone']}
- 位置：{emp['location']}
- 直属经理：{emp['manager']}
        """.strip()
        output_parts.append(emp_info)
    
    return "\n\n".join(output_parts)


@tool
def book_meeting_room(
    room_name: str,
    date: str,
    time: str,
    duration: int,
    booker: str,
    purpose: str
) -> str:
    """
    预订会议室。
    
    Args:
        room_name: 会议室名称（如：A1, A2, B1, B2, C1）
        date: 预订日期（格式：YYYY-MM-DD）
        time: 开始时间（格式：HH:MM，24小时制）
        duration: 会议持续时间（分钟）
        booker: 预订人姓名
        purpose: 会议目的或主题
    
    Returns:
        预订结果
    """
    result = meeting_room_system.book_room(
        room_name=room_name,
        date=date,
        time=time,
        duration=duration,
        booker=booker,
        purpose=purpose
    )
    
    if result["success"]:
        booking = result["booking"]
        # 获取完整的会议室名称
        room_info = meeting_room_system.rooms.get(booking['room_name'], {})
        full_room_name = room_info.get('name', booking['room_name'])
        
        return f"""
 ✅ {result['message']}
 
 【预订详情】
 - 预订号：{booking['booking_id']}
 - 会议室：{full_room_name}
 - 日期：{booking['date']}
 - 时间：{booking['time']}
 - 时长：{booking['duration']} 分钟
 - 预订人：{booking['booker']}
 - 会议目的：{booking['purpose']}
 
 💡 提示：请准时参加会议，如需取消请提前通知行政部。
        """.strip()
    else:
        return f"""
❌ 预订失败

{result['message']}

💡 提示：您可以先查询可用会议室，然后选择其他时间或房间。
        """.strip()


@tool
def query_leave_balance(employee_name: str) -> str:
    """
    查询员工的假期余额，包括年假、病假和事假。
    
    Args:
        employee_name: 员工姓名
    
    Returns:
        假期余额详细信息
    """
    balance_info = leave_system.format_balance_info(employee_name)
    return balance_info


@tool
def get_available_meeting_rooms(
    date: str,
    time: str,
    min_capacity: Optional[int] = None
) -> str:
    """
    查询指定日期时间的可用会议室。
    
    Args:
        date: 查询日期（格式：YYYY-MM-DD）
        time: 查询时间（格式：HH:MM，24小时制）
        min_capacity: 最小容量要求（可选）
    
    Returns:
        可用会议室列表
    """
    available_rooms = meeting_room_system.get_available_rooms(
        date=date,
        time=time,
        capacity=min_capacity
    )
    
    if not available_rooms:
        return f"在 {date} {time} 没有可用的会议室。请尝试其他时间。"
    
    # 格式化结果
    output_parts = ["【可用会议室列表】\n"]
    for room in available_rooms:
        equipment = "、".join(room['equipment'])
        capacity_note = f"（容量：{room['capacity']}人）" if min_capacity else ""
        
        room_info = f"""
📍 {room['name']}{capacity_note}
- 位置：{room['floor']}
- 容量：{room['capacity']} 人
- 设备：{equipment}
        """.strip()
        output_parts.append(room_info)
    
    return "\n".join(output_parts)


# 工具注册列表
API_TOOLS = [
    search_employee_directory,
    book_meeting_room,
    query_leave_balance,
    get_available_meeting_rooms
]
