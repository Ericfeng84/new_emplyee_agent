"""
Tools for Nexus Agent
Company policy lookup, contact information, knowledge base search, and onboarding guide
"""

from typing import Optional
from langchain.tools import tool


@tool
def lookup_company_policy(topic: str) -> str:
    """Look up company policies and procedures.
    
    Args:
        topic: The policy topic to search for (e.g., 'expense', 'leave', 'onboarding')
    
    Returns:
        Information about the requested policy topic
    """
    # Simulated policy lookup - in production, this would query a knowledge base
    policies = {
        "expense": "公司报销政策：员工需要提交费用报销单，附上相关发票，经部门经理审批后提交财务部门。报销周期通常为5-7个工作日。",
        "leave": "请假政策：员工需提前通过HR系统提交请假申请。年假需提前3天申请，病假需提供医疗证明。事假需部门经理审批。",
        "onboarding": "新员工入职流程：1. 完成入职表格 2. 领取设备 3. 参加入职培训 4. 认识团队成员 5. 设置工作环境",
        "it": "IT支持：遇到技术问题请通过IT工单系统提交。紧急问题可拨打IT支持热线：400-XXX-XXXX",
        "benefits": "员工福利：包括五险一金、年度体检、带薪年假、节日福利、团建活动等。详细信息请查阅员工手册。",
        "training": "培训资源：公司提供在线学习平台，包含专业技能培训、管理培训、新员工培训等课程。",
        "default": f"关于'{topic}'的政策信息，建议您查阅员工手册或联系相关部门获取详细信息。"
    }
    
    # Simple keyword matching
    for key in policies:
        if key in topic.lower():
            return policies[key]
    
    return policies["default"]


@tool
def get_contact_info(department: str) -> str:
    """Get contact information for company departments.
    
    Args:
        department: The department name (e.g., 'HR', 'Finance', 'IT')
    
    Returns:
        Contact information for the requested department
    """
    contacts = {
        "hr": "人力资源部：hr@company.com | 内线：1001 | 位置：3楼",
        "finance": "财务部：finance@company.com | 内线：1002 | 位置：4楼",
        "it": "IT支持部：it@company.com | 内线：1003 | 位置：2楼",
        "admin": "行政部：admin@company.com | 内线：1004 | 位置：5楼",
        "legal": "法务部：legal@company.com | 内线：1005 | 位置：6楼",
        "default": f"关于'{department}'部门的联系方式，建议您通过公司通讯录查询。"
    }
    
    for key in contacts:
        if key in department.lower():
            return contacts[key]
    
    return contacts["default"]


@tool
def search_knowledge_base(query: str) -> str:
    """Search the company knowledge base for information.
    
    Args:
        query: The search query
    
    Returns:
        Relevant information from the knowledge base
    """
    # Simulated knowledge base search
    kb_entries = [
        "公司使用Slack进行内部沟通，Teams用于视频会议。",
        "工作时间是周一至周五 9:00-18:00，弹性工作制允许在8:00-10:00之间开始工作。",
        "公司提供免费午餐和下午茶，食堂位于1楼。",
        "新员工有30天的试用期，期间享受完整薪资福利。",
        "公司每季度进行一次绩效评估，年度评估在12月进行。",
        "差旅费用需要提前申请，报销需提供发票和行程单。",
        "员工可以使用公司邮箱（@company.com）和Google Workspace进行协作。"
    ]
    
    # Simple keyword matching
    relevant_entries = []
    query_lower = query.lower()
    
    for entry in kb_entries:
        # Check for any word overlap
        entry_words = set(entry.lower().split())
        query_words = set(query_lower.split())
        if entry_words & query_words:
            relevant_entries.append(entry)
    
    if relevant_entries:
        return "\n".join(relevant_entries[:3])  # Return top 3 matches
    else:
        return f"未找到与'{query}'相关的信息。建议您联系相关部门或查阅员工手册。"


@tool
def get_onboarding_guide(step: Optional[str] = None) -> str:
    """Get onboarding information for new employees.
    
    Args:
        step: Optional specific step (e.g., 'day1', 'week1', 'month1')
    
    Returns:
        Onboarding guide information
    """
    guides = {
        "day1": "第一天入职：1. 到前台报到 2. 领取工牌和设备 3. 参加入职培训 4. 认识导师和团队成员",
        "week1": "第一周目标：1. 完成所有入职培训 2. 设置工作环境 3. 了解团队工作流程 4. 开始接触实际项目",
        "month1": "第一个月目标：1. 熟悉公司系统和工具 2. 完成第一个小任务 3. 建立团队关系 4. 参加团队活动",
        "default": "新员工入职指南：\n- 第一天：报到、领取设备、入职培训\n- 第一周：完成培训、设置环境、了解流程\n- 第一个月：熟悉系统、完成任务、建立关系\n- 持续：学习成长、融入团队、贡献价值"
    }
    
    if step:
        return guides.get(step.lower(), guides["default"])
    return guides["default"]


# Tool registry for easy access
NEXUS_TOOLS = [
    lookup_company_policy,
    get_contact_info,
    search_knowledge_base,
    get_onboarding_guide
]
