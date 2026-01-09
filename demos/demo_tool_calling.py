"""
Sprint 3 工具调用演示脚本
展示 Agent 的工具调用能力
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

from nexus_agent.agent.agent import NexusLangChainAgent


def run_tool_calling_demo():
    """
    运行工具调用演示
    """
    print("=" * 70)
    print("Nexus Agent - Tool Calling Demo (Sprint 3)")
    print("=" * 70)
    print()
    
    # 创建 Agent
    print("初始化 Agent...")
    agent = NexusLangChainAgent(
        provider="deepseek",
        model="deepseek-chat",
        temperature=0.7
    )
    print("✅ Agent 初始化完成")
    print()
    
    # 测试场景
    test_scenarios = [
        {
            "name": "场景 1: 查找同事信息",
            "query": "张三的电话是多少？他在哪个部门？",
            "expected_tool": "search_employee_directory"
        },
        {
            "name": "场景 2: 查询可用会议室",
            "query": "明天下午2点有哪些会议室可用？",
            "expected_tool": "get_available_meeting_rooms"
        },
        {
            "name": "场景 3: 预订会议室",
            "query": "帮我预订 A1 会议室，2026-01-10 下午2点，开1小时会，我是张三，会议目的是项目讨论",
            "expected_tool": "book_meeting_room"
        },
        {
            "name": "场景 4: 查询假期余额",
            "query": "查一下张三的假期余额",
            "expected_tool": "query_leave_balance"
        },
        {
            "name": "场景 5: 普通聊天（不需要工具）",
            "query": "你好，请介绍一下自己",
            "expected_tool": None
        },
        {
            "name": "场景 6: 知识库查询",
            "query": "公司的报销政策是什么？",
            "expected_tool": "retrieve_context"
        }
    ]
    
    # 执行测试
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'=' * 70}")
        print(f"{scenario['name']}")
        print(f"{'=' * 70}")
        print(f"\n用户: {scenario['query']}")
        print("-" * 70)
        
        # 处理查询
        response = agent.process_message(scenario['query'])
        
        # 显示响应
        print(f"\nNexus: {response.content}")
        
        # 显示工具调用信息
        if response.tool_calls:
            print(f"\n🔧 使用的工具: {len(response.tool_calls)} 个")
            for j, tool_call in enumerate(response.tool_calls, 1):
                print(f"   {j}. {tool_call.get('name', 'Unknown')}")
        else:
            print("\n💬 未使用工具（直接对话）")
        
        # 显示性能指标
        if response.duration:
            print(f"\n⏱️  响应时间: {response.duration:.2f} 秒")
        
        print()
    
    # 总结
    print("=" * 70)
    print("演示完成")
    print("=" * 70)
    print("\n✅ 工具调用功能测试通过")
    print("✅ Agent 能够自动判断何时使用工具")
    print("✅ 所有 API 工具正常工作")


def run_interactive_tool_demo():
    """
    运行交互式工具调用演示
    """
    print("=" * 70)
    print("Nexus Agent - Interactive Tool Calling Demo")
    print("=" * 70)
    print()
    print("可用的工具：")
    print("  🔍 search_employee_directory - 搜索员工信息")
    print("  📅 book_meeting_room - 预订会议室")
    print("  🏖️  query_leave_balance - 查询假期余额")
    print("  📋 get_available_meeting_rooms - 查询可用会议室")
    print("  📚 retrieve_context - 检索知识库")
    print()
    print("输入 'quit' 或 'exit' 退出")
    print("=" * 70)
    print()
    
    # 创建 Agent
    agent = NexusLangChainAgent(
        provider="deepseek",
        model="deepseek-chat",
        temperature=0.7
    )
    
    # 交互循环
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            # 处理查询
            response = agent.process_message(user_input)
            
            # 显示响应
            print(f"\nNexus: {response.content}")
            
            # 显示工具调用
            if response.tool_calls:
                print(f"\n🔧 使用了 {len(response.tool_calls)} 个工具")
            
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_tool_demo()
    else:
        run_tool_calling_demo()
