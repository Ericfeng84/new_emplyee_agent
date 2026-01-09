# Sprint 4: 记忆管理与多轮对话 - 快速开始指南

## 🎯 Sprint 目标

实现像人一样的连续对话能力，为 Nexus Agent 添加持久化记忆管理能力，使其能够：
- 记住用户的历史对话
- 区分不同用户的会话
- 实现长对话的上下文管理
- 通过 Redis 持久化存储和智能上下文压缩

## ✅ 实现状态

### 核心组件

| 组件 | 状态 | 文件 |
|------|------|------|
| Redis 客户端 | ✅ 完成 | [`nexus_agent/storage/redis_client.py`](../nexus_agent/storage/redis_client.py) |
| 会话管理器 | ✅ 完成 | [`nexus_agent/storage/session_manager.py`](../nexus_agent/storage/session_manager.py) |
| 上下文管理器 | ✅ 完成 | [`nexus_agent/storage/context_manager.py`](../nexus_agent/storage/context_manager.py) |
| Agent 集成 | ✅ 完成 | [`nexus_agent/agent/agent.py`](../nexus_agent/agent/agent.py) |
| 配置管理 | ✅ 完成 | [`nexus_agent/config/settings.py`](../nexus_agent/config/settings.py) |
| 演示脚本 | ✅ 完成 | [`demo_memory_management.py`](../demo_memory_management.py) |
| 文档 | ✅ 完成 | [`sprint4-memory-management-implementation.md`](./sprint4-memory-management-implementation.md) |

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 UV 安装依赖
uv sync
```

### 2. 配置 Redis

#### 方法 A: 使用本地 Redis

```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:latest
```

#### 方法 B: 使用云 Redis

在 [`.env`](../.env) 文件中配置：

```bash
REDIS_HOST=your-redis-host.com
REDIS_PORT=6379
REDIS_PASSWORD=your-password
```

### 3. 配置环境变量

复制 [`.env.example`](../.env.example) 到 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加你的 API 密钥：

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 4. 运行演示

#### 自动化演示

```bash
python demo_memory_management.py
```

这将演示：
- 创建新会话
- 多轮对话（Agent 记住用户信息）
- 查看对话历史
- 上下文压缩测试
- 多个独立会话
- 会话管理

#### 交互式演示

```bash
python demo_memory_management.py --interactive
```

交互式命令：
- 直接输入消息 - 与 Agent 对话
- `new` - 创建新会话
- `switch <session_id>` - 切换会话
- `history` - 查看当前会话历史
- `info` - 查看当前会话信息
- `clear` - 清空当前会话历史
- `sessions` - 列出所有会话
- `quit` 或 `exit` - 退出

## 💻 代码示例

### 基本使用

```python
from nexus_agent.agent.agent import NexusLangChainAgent

# 创建 Agent（启用记忆）
agent = NexusLangChainAgent(
    provider="deepseek",
    model="deepseek-chat",
    temperature=0.7,
    enable_memory=True  # 启用记忆功能
)

# 第一次对话，自动创建新会话
response = agent.process_message("你好，我叫张三")
session_id = response.session_id
print(f"Session ID: {session_id}")

# 继续对话，Agent 会记住之前的对话
response = agent.process_message(
    "我叫什么名字？",
    session_id=session_id
)
print(response.content)
```

### 多用户会话

```python
# 用户 A 的会话
response_a = agent.process_message(
    "我是用户A",
    user_id="user_a"
)
session_id_a = response_a.session_id

# 用户 B 的会话
response_b = agent.process_message(
    "我是用户B",
    user_id="user_b"
)
session_id_b = response_b.session_id

# 两个会话完全独立
```

### 查看对话历史

```python
# 获取对话历史
history = agent.get_conversation_history(session_id)
print(f"历史消息数: {len(history)}")

for msg in history:
    print(f"[{msg['role']}] {msg['content']}")
```

### 会话管理

```python
# 获取会话信息
session_info = agent.get_session_info(session_id)
print(f"消息数: {session_info['message_count']}")
print(f"创建时间: {session_info['created_at']}")

# 清空会话历史
agent.clear_session(session_id)

# 删除会话
agent.delete_session(session_id)
```

## 📊 架构概览

```
用户输入
    ↓
NexusLangChainAgent (enable_memory=True)
    ↓
检查 Session ID
    ↓
    ├─ 新会话 → 创建新 Session (UUID)
    └─ 已有会话 → 加载历史对话
         ↓
    上下文管理器
         ↓
    Token 预算检查
         ↓
    ├─ 未超限 → 完整历史
    └─ 超限 → 上下文压缩
         ↓
    LLM 处理
         ↓
    生成响应
         ↓
    保存到 Redis
    ├─ 保存用户消息
    └─ 保存助手响应
         ↓
    返回响应（包含 session_id）
```

## 🔧 配置选项

### Redis 配置

```bash
REDIS_HOST=localhost          # Redis 服务器地址
REDIS_PORT=6379              # Redis 端口
REDIS_DB=0                   # Redis 数据库编号
REDIS_PASSWORD=                # Redis 密码（可选）
```

### 会话管理配置

```bash
SESSION_TTL=604800           # 会话过期时间（秒），默认 7 天
MAX_HISTORY_LENGTH=100         # 最大历史消息数
MAX_CONTEXT_TOKENS=4000       # 最大上下文 Token 数
CONTEXT_COMPRESSION_THRESHOLD=0.8  # 压缩阈值
```

## 📚 文档

- [完整实现文档](./sprint4-memory-management-implementation.md)
- [原始计划文档](../plans/sprint4-memory-management-plan.md)
- [Redis 客户端实现](../nexus_agent/storage/redis_client.py)
- [会话管理器实现](../nexus_agent/storage/session_manager.py)
- [上下文管理器实现](../nexus_agent/storage/context_manager.py)

## 🧪 测试

### 运行现有测试

```bash
# 运行所有测试
pytest nexus_agent/tests/

# 运行特定测试
pytest nexus_agent/tests/test_conversation.py
```

### 注意事项

单元测试（test_redis_client.py, test_session_manager.py, test_context_manager.py, test_memory_integration.py）需要在后续 Sprint 中实现。

## 🔒 安全考虑

- 会话使用唯一 UUID 标识
- 用户 ID 可选，用于用户级隔离
- 所有会话数据自动过期（默认 7 天）
- 建议在生产环境中添加认证机制

## 📈 性能优化

- Redis 连接池管理
- 两级上下文压缩策略
- 自动限制历史消息数量
- Token 预算智能管理

## 🐛 故障排查

### Redis 连接失败

```bash
# 检查 Redis 是否运行
redis-cli ping

# 启动 Redis
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

### Token 计数不准确

```bash
# 确认 tiktoken 已安装
uv pip list | grep tiktoken
```

### 会话丢失

检查 TTL 设置和 Redis 内存使用：

```bash
redis-cli info memory
```

## 🎯 下一步

Sprint 4 已完成核心记忆管理功能。建议后续工作：

1. 实现完整的单元测试套件
2. 添加会话认证和授权
3. 实现更智能的上下文压缩策略
4. 添加对话摘要功能
5. 实现会话导出和导入

## 📝 总结

✅ **已完成：**
- Redis 持久化存储
- 会话管理系统
- 对话历史管理
- 上下文管理器
- Agent 集成
- 演示脚本
- 完整文档

🔄 **待完成：**
- 单元测试套件
- 会话认证机制
- 高级压缩策略

---

**Sprint 状态：** ✅ 核心功能已完成
**最后更新：** 2026-01-08
