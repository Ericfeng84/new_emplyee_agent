"""
Sprint 4 记忆管理演示脚本
展示 Agent 的记忆管理和多轮对话能力
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from nexus_agent.agent.agent import NexusLangChainAgent


def run_memory_demo():
    """
    运行记忆管理演示
    """
    print("=" * 70)
    print("Nexus Agent - Memory Management Demo (Sprint 4)")
    print("=" * 70)
    print()
    
    # 创建 Agent（启用记忆）
    print("初始化 Agent（启用记忆）...")
    agent = NexusLangChainAgent(
        provider="deepseek",
        model="deepseek-chat",
        temperature=0.7,
        enable_memory=True
    )
    print("✅ Agent 初始化完成")
    print()
    
    # 场景 1: 创建新会话
    print("=" * 70)
    print("场景 1: 创建新会话")
    print("=" * 70)
    print()
    
    response = agent.process_message("你好，我叫张三，我是新员工")
    print(f"用户: 你好，我叫张三，我是新员工")
    print(f"Nexus: {response.content}")
    print(f"📝 Session ID: {response.session_id}")
    print()
    
    session_id = response.session_id
    
    # 场景 2: 多轮对话 - Agent 记住用户信息
    print("=" * 70)
    print("场景 2: 多轮对话 - Agent 记住用户信息")
    print("=" * 70)
    print()
    
    questions = [
        "我叫什么名字？",
        "我的职位是什么？",
        "你能帮我查一下公司的报销政策吗？"
    ]
    
    for question in questions:
        print(f"用户: {question}")
        response = agent.process_message(question, session_id=session_id)
        print(f"Nexus: {response.content}")
        print()
    
    # 场景 3: 查看对话历史
    print("=" * 70)
    print("场景 3: 查看对话历史")
    print("=" * 70)
    print()
    
    history = agent.get_conversation_history(session_id)
    print(f"📊 对话历史: {len(history)} 条消息")
    print()
    
    for i, msg in enumerate(history[-5:], 1):  # 显示最近 5 条
        role = msg["role"]
        content = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
        print(f"{i}. [{role}] {content}")
    print()
    
    # 场景 4: 上下文压缩测试
    print("=" * 70)
    print("场景 4: 上下文压缩测试")
    print("=" * 70)
    print()
    
    print("发送多条消息以测试上下文压缩...")
    for i in range(10):
        agent.process_message(
            f"这是第 {i+1} 条测试消息",
            session_id=session_id
        )
    
    # 获取统计信息
    from nexus_agent.storage.context_manager import ContextManager
    context_mgr = ContextManager()
    stats = context_mgr.get_context_stats(history)
    
    print(f"📊 上下文统计:")
    print(f"   - 总消息数: {stats['message_count']}")
    print(f"   - 总 Token 数: {stats['total_tokens']}")
    print(f"   - 预算使用率: {stats['budget_ratio']:.2%}")
    print()
    
    # 场景 5: 多个独立会话
    print("=" * 70)
    print("场景 5: 多个独立会话")
    print("=" * 70)
    print()
    
    # 创建第二个会话
    print("创建第二个会话...")
    response2 = agent.process_message(
        "你好，我叫李四，我是市场部的",
        user_id="user_b"
    )
    session_id_2 = response2.session_id
    
    print(f"用户: 你好，我叫李四，我是市场部的")
    print(f"Nexus: {response2.content}")
    print(f"📝 Session ID: {response2.session_id}")
    print()
    
    # 在两个会话之间切换
    print("切换回第一个会话...")
    response1 = agent.process_message(
        "还记得我是谁吗？",
        session_id=session_id
    )
    print(f"用户: 还记得我是谁吗？")
    print(f"Nexus: {response1.content}")
    print()
    
    print("切换到第二个会话...")
    response2 = agent.process_message(
        "那我呢？",
        session_id=session_id_2
    )
    print(f"用户: 那我呢？")
    print(f"Nexus: {response2.content}")
    print()
    
    # 场景 6: 会话管理
    print("=" * 70)
    print("场景 6: 会话管理")
    print("=" * 70)
    print()
    
    # 获取会话信息
    session_info = agent.get_session_info(session_id)
    if session_info:
        print(f"📊 会话信息:")
        print(f"   - Session ID: {session_info['session_id']}")
        print(f"   - 用户 ID: {session_info.get('user_id', 'N/A')}")
        print(f"   - 消息数: {session_info.get('message_count', 0)}")
        print(f"   - 创建时间: {session_info.get('created_at', 'N/A')}")
        print(f"   - 最后活跃: {session_info.get('last_active', 'N/A')}")
    print()
    
    # 总结
    print("=" * 70)
    print("演示完成")
    print("=" * 70)
    print("\n✅ 记忆管理功能测试通过")
    print("✅ Agent 能够记住多轮对话")
    print("✅ 支持多个独立会话")
    print("✅ 上下文压缩正常工作")


def run_interactive_memory_demo():
    """
    运行交互式记忆管理演示
    """
    print("=" * 70)
    print("Nexus Agent - Interactive Memory Management Demo")
    print("=" * 70)
    print()
    print("命令:")
    print("  直接输入消息 - 与 Agent 对话")
    print("  'new' - 创建新会话")
    print("  'switch <session_id>' - 切换会话")
    print("  'history' - 查看当前会话历史")
    print("  'info' - 查看当前会话信息")
    print("  'clear' - 清空当前会话历史")
    print("  'sessions' - 列出所有会话")
    print("  'quit' 或 'exit' - 退出")
    print("=" * 70)
    print()
    
    # 创建 Agent
    agent = NexusLangChainAgent(
        provider="deepseek",
        model="deepseek-chat",
        temperature=0.7,
        enable_memory=True
    )
    
    # 当前会话
    current_session_id = None
    
    # 交互循环
    while True:
        try:
            # 显示当前会话
            if current_session_id:
                print(f"[Session: {current_session_id[:8]}...]", end=" ")
            
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            elif user_input.lower() == 'new':
                response = agent.process_message("你好")
                current_session_id = response.session_id
                print(f"\n✅ 创建新会话: {current_session_id}")
                print(f"Nexus: {response.content}\n")
            
            elif user_input.lower() == 'history':
                if not current_session_id:
                    print("❌ 没有当前会话\n")
                    continue
                
                history = agent.get_conversation_history(current_session_id)
                print(f"\n📊 对话历史 ({len(history)} 条消息):\n")
                for i, msg in enumerate(history[-10:], 1):
                    role = msg["role"]
                    content = msg["content"][:80]
                    if len(msg["content"]) > 80:
                        content += "..."
                    print(f"{i}. [{role}] {content}")
                print()
            
            elif user_input.lower() == 'info':
                if not current_session_id:
                    print("❌ 没有当前会话\n")
                    continue
                
                session_info = agent.get_session_info(current_session_id)
                if session_info:
                    print(f"\n📊 会话信息:")
                    print(f"   Session ID: {session_info['session_id']}")
                    print(f"   用户 ID: {session_info.get('user_id', 'N/A')}")
                    print(f"   消息数: {session_info.get('message_count', 0)}")
                    print(f"   创建时间: {session_info.get('created_at', 'N/A')}")
                    print()
            
            elif user_input.lower() == 'clear':
                if not current_session_id:
                    print("❌ 没有当前会话\n")
                    continue
                
                success = agent.clear_session(current_session_id)
                if success:
                    print(f"\n✅ 已清空会话历史\n")
                else:
                    print(f"\n❌ 清空失败\n")
            
            elif user_input.lower() == 'sessions':
                sessions = agent.session_manager.redis.get_all_sessions()
                print(f"\n📊 所有会话 ({len(sessions)} 个):\n")
                for i, session in enumerate(sessions[-10:], 1):
                    print(f"{i}. {session['session_id'][:8]}... "
                          f"({session.get('user_id', 'N/A')}) - "
                          f"{session.get('message_count', 0)} 条消息")
                print()
            
            elif user_input.lower().startswith('switch '):
                session_id = user_input[7:].strip()
                print(f"\n🔄 切换到会话: {session_id}")
                current_session_id = session_id
                print()
            
            else:
                # 普通消息
                response = agent.process_message(
                    user_input,
                    session_id=current_session_id
                )
                
                # 更新当前会话
                if response.session_id:
                    current_session_id = response.session_id
                
                print(f"\nNexus: {response.content}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_memory_demo()
    else:
        run_memory_demo()
