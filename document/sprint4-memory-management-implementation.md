# Sprint 4: 记忆管理与多轮对话 - 实现文档

## 📋 概述

Sprint 4 实现了 Nexus Agent 的持久化记忆管理能力，使其能够记住用户的历史对话，区分不同用户的会话，并实现长对话的上下文管理。通过 Redis 持久化存储和智能上下文压缩，让 Agent 具备真正的"记忆"。

**状态：** ✅ 已完成
**实现日期：** 2026-01-08

---

## 🏗️ 架构设计

### 整体架构

```
用户输入 → NexusLangChainAgent
    ↓
检查 Session ID
    ↓
    ├─ 新会话 → 创建新 Session
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
         ↓
    返回响应
```

### 核心组件

#### 1. Redis 客户端 ([`nexus_agent/storage/redis_client.py`](../nexus_agent/storage/redis_client.py))

负责与 Redis 服务器通信，提供持久化存储能力。

**主要功能：**
- 连接池管理
- 会话信息存储和检索
- 对话历史管理
- 自动过期机制

**关键方法：**
- `get_session(session_id)` - 获取会话信息
- `save_session(session_id, session_data)` - 保存会话信息
- `get_conversation_history(session_id, limit)` - 获取对话历史
- `add_message(session_id, role, content, metadata)` - 添加消息
- `clear_history(session_id)` - 清空历史
- `delete_session(session_id)` - 删除会话

#### 2. 会话管理器 ([`nexus_agent/storage/session_manager.py`](../nexus_agent/storage/session_manager.py))

管理用户会话的生命周期和对话历史。

**主要功能：**
- 创建和管理会话
- 会话 ID 生成（UUID）
- 消息计数和活跃时间更新
- 用户会话隔离

**关键方法：**
- `create_session(user_id, metadata)` - 创建新会话
- `get_session(session_id)` - 获取会话信息
- `update_session(session_id, **kwargs)` - 更新会话
- `increment_message_count(session_id)` - 增加消息计数
- `add_message(session_id, role, content, metadata)` - 添加消息
- `get_conversation_history(session_id, limit)` - 获取历史

#### 3. 上下文管理器 ([`nexus_agent/storage/context_manager.py`](../nexus_agent/storage/context_manager.py))

管理对话上下文和 Token 预算，实现智能压缩。

**主要功能：**
- Token 计数（使用 tiktoken）
- Token 预算检查
- 上下文压缩策略
- 消息格式化

**关键方法：**
- `count_tokens(text)` - 计算文本 Token 数
- `count_messages_tokens(messages)` - 计算消息列表 Token 数
- `check_token_budget(messages, max_tokens)` - 检查是否超限
- `compress_context(messages, max_tokens)` - 压缩上下文
- `format_messages_for_llm(messages)` - 格式化消息

#### 4. Agent 集成 ([`nexus_agent/agent/agent.py`](../nexus_agent/agent/agent.py))

将记忆管理功能集成到 Nexus Agent 中。

**新增功能：**
- `enable_memory` 参数控制是否启用记忆
- `session_id` 参数用于会话管理
- 自动创建和管理会话
- 自动保存对话历史

**新增方法：**
- `get_session_info(session_id)` - 获取会话信息
- `get_conversation_history(session_id, limit)` - 获取对话历史
- `clear_session(session_id)` - 清空会话历史
- `delete_session(session_id)` - 删除会话
- `_build_messages(user_message, history)` - 构建消息列表

---

## 📝 配置说明

### Redis 配置

在 [`.env`](../.env) 文件中配置 Redis 连接：

```bash
# Redis Configuration
REDIS_HOST=localhost          # Redis 服务器地址
REDIS_PORT=6379              # Redis 端口
REDIS_DB=0                   # Redis 数据库编号
REDIS_PASSWORD=                # Redis 密码（可选）
```

### 会话管理配置

```bash
# Session Management
SESSION_TTL=604800           # 会话过期时间（秒），默认 7 天
MAX_HISTORY_LENGTH=100         # 最大历史消息数
MAX_CONTEXT_TOKENS=4000       # 最大上下文 Token 数
CONTEXT_COMPRESSION_THRESHOLD=0.8  # 压缩阈值
```

### 使用配置

在 [`nexus_agent/config/settings.py`](../nexus_agent/config/settings.py) 中：

```python
class NexusConfig(BaseSettings):
    # Redis Configuration
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    redis_password: Optional[str] = Field(default=None)
    
    # Session Management Configuration
    session_ttl: int = Field(default=60 * 60 * 24 * 7)  # 7天
    max_history_length: int = Field(default=100)
    max_context_tokens: int = Field(default=4000)
    context_compression_threshold: float = Field(default=0.8)
```

---

## 🚀 使用指南

### 基本使用

#### 1. 启用记忆功能的 Agent

```python
from nexus_agent.agent.agent import NexusLangChainAgent

# 创建 Agent（启用记忆）
agent = NexusLangChainAgent(
    provider="deepseek",
    model="deepseek-chat",
    temperature=0.7,
    enable_memory=True  # 启用记忆功能
)
```

#### 2. 创建新会话

```python
# 第一次对话，自动创建新会话
response = agent.process_message("你好，我叫张三")
session_id = response.session_id
print(f"Session ID: {session_id}")
```

#### 3. 继续对话

```python
# 使用相同的 session_id 继续对话
response = agent.process_message(
    "我叫什么名字？",
    session_id=session_id
)
print(response.content)
```

#### 4. 查看对话历史

```python
# 获取对话历史
history = agent.get_conversation_history(session_id)
print(f"历史消息数: {len(history)}")

for msg in history:
    print(f"[{msg['role']}] {msg['content']}")
```

#### 5. 会话管理

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

### 高级使用

#### 1. 多用户会话

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

#### 2. 上下文压缩

当对话历史过长时，系统会自动压缩上下文：

```python
# 发送大量消息
for i in range(100):
    agent.process_message(
        f"消息 {i}",
        session_id=session_id
    )

# 系统自动压缩，保留最近的重要消息
```

压缩策略：
1. 优先保留最近的 N 条消息
2. 保留系统消息
3. 如果仍然超限，只保留最近 5 条

#### 3. 上下文统计

```python
from nexus_agent.storage.context_manager import ContextManager

context_mgr = ContextManager()
history = agent.get_conversation_history(session_id)

# 获取上下文统计
stats = context_mgr.get_context_stats(history)
print(f"总 Token 数: {stats['total_tokens']}")
print(f"消息数: {stats['message_count']}")
print(f"预算使用率: {stats['budget_ratio']:.2%}")
print(f"是否超限: {stats['is_over_budget']}")
```

---

## 📊 数据结构

### Redis 数据结构

#### 会话信息

Key: `session:{session_id}`
Type: String (JSON)
TTL: 7 天

```json
{
    "session_id": "uuid",
    "user_id": "user123",
    "created_at": "2026-01-08T12:00:00",
    "last_active": "2026-01-08T12:05:00",
    "message_count": 10,
    "metadata": {}
}
```

#### 对话历史

Key: `history:{session_id}`
Type: List (Redis List)
TTL: 7 天

每个消息元素：

```json
{
    "role": "user|assistant|system",
    "content": "消息内容",
    "timestamp": "2026-01-08T12:00:00",
    "metadata": {
        "tool_calls": [],
        "duration": 1.5
    }
}
```

---

## 🧪 测试

### 运行演示脚本

#### 自动化演示

```bash
python demo_memory_management.py
```

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

### 单元测试

```bash
# 运行所有测试
pytest nexus_agent/tests/

# 运行特定测试
pytest nexus_agent/tests/test_redis_client.py
pytest nexus_agent/tests/test_session_manager.py
pytest nexus_agent/tests/test_context_manager.py
pytest nexus_agent/tests/test_memory_integration.py
```

---

## 🔧 故障排查

### Redis 连接失败

**问题：** `❌ Redis 连接失败`

**解决方案：**
1. 检查 Redis 是否运行：
   ```bash
   redis-cli ping
   # 应该返回 PONG
   ```

2. 检查配置：
   ```bash
   # 确认 .env 文件中的配置
   cat .env | grep REDIS
   ```

3. 启动 Redis（如果未运行）：
   ```bash
   # macOS
   brew services start redis
   
   # Linux
   sudo systemctl start redis
   
   # Docker
   docker run -d -p 6379:6379 redis:latest
   ```

### Token 计数不准确

**问题：** 上下文压缩不准确

**解决方案：**
1. 确认 tiktoken 已正确安装：
   ```bash
   uv pip list | grep tiktoken
   ```

2. 检查使用的编码：
   ```python
   import tiktoken
   encoding = tiktoken.encoding_for_model("gpt-4")
   print(encoding.name)
   ```

### 会话丢失

**问题：** 会话数据意外丢失

**解决方案：**
1. 检查 TTL 设置：
   ```python
   from nexus_agent.config.settings import config
   print(f"Session TTL: {config.session_ttl} seconds")
   ```

2. 检查 Redis 内存：
   ```bash
   redis-cli info memory
   ```

3. 调整 TTL 配置（如果需要）：
   ```bash
   # 在 .env 中
   SESSION_TTL=1209600  # 14 天
   ```

---

## 📈 性能优化

### Redis 连接池

已实现连接池管理，避免频繁创建和销毁连接：

```python
from redis.connection import ConnectionPool

self.pool = ConnectionPool(
    host=config.redis_host,
    port=config.redis_port,
    max_connections=50,  # 最大连接数
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True
)
```

### 上下文压缩策略

采用两级压缩策略：

1. **第一级：保留最近消息**
   - 从最新的消息开始，逐步添加
   - 直到接近 Token 预算

2. **第二级：生成摘要**
   - 保留系统消息
   - 保留最近 10 条消息
   - 如果仍然超限，只保留最近 5 条

### 消息限制

自动限制历史消息数量，防止无限增长：

```python
# 限制历史长度
max_length = config.max_history_length  # 默认 100
if max_length:
    self.client.ltrim(key, 0, max_length - 1)
```

---

## 🔒 安全考虑

### 会话隔离

- 每个会话使用唯一的 UUID
- 用户 ID 可选，用于用户级隔离
- 会话数据完全独立

### 数据过期

- 所有会话数据自动过期（默认 7 天）
- 避免数据无限累积
- 可配置 TTL

### 访问控制

- Session ID 是访问会话的唯一凭证
- 需要妥善保管 Session ID
- 建议在生产环境中添加认证机制

---

## 📚 相关文档

- [Sprint 4 计划文档](../plans/sprint4-memory-management-plan.md)
- [Redis 客户端实现](../nexus_agent/storage/redis_client.py)
- [会话管理器实现](../nexus_agent/storage/session_manager.py)
- [上下文管理器实现](../nexus_agent/storage/context_manager.py)
- [Agent 集成实现](../nexus_agent/agent/agent.py)
- [配置说明](../.env.example)

---

## 🎯 总结

Sprint 4 成功实现了 Nexus Agent 的记忆管理功能，包括：

✅ **Redis 持久化存储**
- 连接池管理
- 会话信息存储
- 对话历史管理

✅ **会话管理系统**
- Session ID 机制
- 会话创建和管理
- 用户会话隔离

✅ **对话历史管理**
- 消息存储和检索
- 历史查询
- 会话清理

✅ **上下文管理器**
- Token 计数
- 上下文压缩
- 预算管理

✅ **Agent 集成**
- 记忆功能开关
- 会话传递
- 历史加载

✅ **演示和文档**
- 自动化演示脚本
- 交互式演示脚本
- 完整的使用文档

---

**文档版本：** 1.0
**最后更新：** 2026-01-08
