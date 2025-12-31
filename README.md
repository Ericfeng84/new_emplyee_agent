# Nexus Agent - 新员工入职助手

基于 LangChain 1.0 的智能对话系统，专为帮助新员工快速适应工作环境而设计。

## 📋 项目概述

Nexus Agent 是一个专注于新员工入职支持的 AI 助手，通过自然语言对话提供工作相关的指导和帮助。该项目采用 LangChain 1.0 的 `create_agent` API，结合中间件架构实现安全检查、动态模型选择和工具调用能力。

### 核心特性

- 🔒 **安全可靠**: 内置输入/输出验证，防止提示注入和敏感信息泄露
- 🤖 **多提供商支持**: 支持 OpenAI、DeepSeek、Qwen 等多种 LLM 提供商
- 💬 **多轮对话**: 支持上下文感知的多轮对话
- 🛠️ **工具调用**: 内置公司政策查询、联系方式获取等工具
- 📊 **监控追踪**: 完整的日志记录和 Token 使用追踪
- 🧪 **测试完善**: 包含全面的安全测试和对话流程测试
- 🔧 **易于配置**: 通过环境变量灵活配置
- ⚡ **中间件架构**: 使用 LangChain 1.0 中间件模式，模块化可扩展

## 🚀 快速开始

### 环境要求

- Python 3.12 或更高版本
- UV 包管理器（推荐）或 pip

### 安装步骤

#### 使用 UV（推荐）

1. **安装 UV**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip
pip install uv
```

2. **克隆项目**
```bash
git clone <repository-url>
cd new_emplyee_agent
```

3. **使用 UV 安装依赖**
```bash
# 创建虚拟环境并安装依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

#### 使用 pip（传统方式）

1. **克隆项目**
```bash
git clone <repository-url>
cd new_emplyee_agent
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -e .
```

4. **配置环境变量**
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：
```env
# 至少配置一个 API 密钥
OPENAI_API_KEY=your_openai_api_key_here
# 或
DEEPSEEK_API_KEY=your_deepseek_api_key_here
# 或
QWEN_API_KEY=your_qwen_api_key_here

# 其他配置（可选）
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
TEMPERATURE=0.7
```

5. **运行演示**
```bash
python demo_script.py
```

## 📖 使用指南

### 基本用法

```python
from nexus_agent.agent.agent import create_nexus_agent

# 创建 agent
agent = create_nexus_agent()

# 发送消息
response = agent.process_message("你好，我是新员工")
print(response.content)
```

### 交互式对话

```python
from nexus_agent.agent.agent import NexusLangChainAgent

agent = NexusLangChainAgent()
agent.interactive_chat()
```

### 流式响应

```python
from nexus_agent.agent.agent import create_nexus_agent

agent = create_nexus_agent()

# 流式处理消息
for chunk in agent.stream_message("请介绍一下公司的报销政策"):
    if chunk["type"] == "message":
        print(chunk["content"], end="", flush=True)
    elif chunk["type"] == "tool_calls":
        print(f"\n[使用了工具: {len(chunk['tool_calls'])} 个]")
```

### 自定义配置

```python
from nexus_agent.agent.agent import NexusLangChainAgent

# 使用自定义配置
agent = NexusLangChainAgent(
    provider="deepseek",
    model="deepseek-chat",
    temperature=0.5,
    enable_safety_checks=True
)
```

### 使用用户偏好

```python
from nexus_agent.agent.agent import create_nexus_agent

agent = create_nexus_agent()

# 为新员工提供详细解释
response = agent.process_message(
    "我应该如何申请年假？",
    user_preferences={"role": "new_employee"}
)

# 为管理者提供简洁回答
response = agent.process_message(
    "年假政策是什么？",
    user_preferences={"role": "manager"}
)
```

### 获取 Agent 信息

```python
from nexus_agent.agent.agent import create_nexus_agent

agent = create_nexus_agent()

# 获取 agent 配置信息
info = agent.get_agent_info()
print(f"Provider: {info['provider']}")
print(f"Model: {info['model']}")
print(f"Tools: {info['tools']}")
print(f"Middleware count: {info['middleware_count']}")
```

## 🏗️ 项目结构

```
nexus-agent/
├── nexus_agent/
│   ├── agent/              # 核心 Agent 模块
│   │   ├── agent.py        # 主 Agent 实现（使用 create_agent）
│   │   ├── middleware.py   # 中间件实现
│   │   ├── state.py        # 状态管理
│   │   ├── tools.py        # 工具定义
│   │   ├── prompts.py      # 系统提示词
│   │   └── __init__.py
│   ├── config/             # 配置管理
│   │   ├── settings.py     # 配置类
│   │   └── __init__.py
│   ├── tests/              # 测试套件
│   │   ├── test_prompts.py      # 提示词安全测试
│   │   ├── test_conversation.py # 对话流程测试
│   │   └── __init__.py
│   ├── utils/              # 工具模块
│   │   ├── logger.py       # 日志工具
│   │   ├── validators.py   # 输入/输出验证
│   │   └── __init__.py
│   └── __init__.py
├── plans/                  # 项目规划文档
│   ├── sprint1-prototype-plan.md
│   └── langchain-1.0-syntax-guide.md
├── demo_script.py          # 演示脚本
├── main.py                 # 主入口
├── pyproject.toml          # 项目配置
├── .env.example           # 环境变量示例
├── README.md              # 项目文档
└── PROJECT_GUIDE.md       # 学习指南
```

## ⚙️ 配置选项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `LLM_PROVIDER` | LLM 提供商 (openai/deepseek/qwen) | openai |
| `LLM_MODEL` | 模型名称 | gpt-4o |
| `TEMPERATURE` | 响应随机性 (0.0-2.0) | 0.7 |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |
| `QWEN_API_KEY` | Qwen API 密钥 | - |
| `LOG_LEVEL` | 日志级别 (DEBUG/INFO/WARNING/ERROR) | INFO |
| `LOG_FILE` | 日志文件路径（可选） | - |
| `ENABLE_SAFETY_CHECKS` | 启用安全检查 | true |
| `MAX_CONVERSATION_LENGTH` | 最大对话历史长度 | 10 |
| `MAX_RETRIES` | 最大重试次数 | 3 |
| `RETRY_DELAY` | 重试延迟（秒） | 1.0 |
| `MAX_TOKENS` | 最大 Token 数 | 1000 |

## 🧪 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试文件
```bash
pytest nexus_agent/tests/test_prompts.py
pytest nexus_agent/tests/test_conversation.py
```

### 运行特定测试
```bash
pytest nexus_agent/tests/test_prompts.py::TestPromptSafety::test_role_boundary_enforcement
```

### 查看详细输出
```bash
pytest -v
```

### 查看测试覆盖率
```bash
pytest --cov=nexus_agent --cov-report=html
```

## 📊 安全机制

### 中间件架构

Nexus Agent 使用 LangChain 1.0 的中间件架构实现安全检查：

1. **NexusPromptMiddleware**: 动态生成系统提示词
2. **SafetyMiddleware**: 输入/输出验证
3. **NexusModelSelectionMiddleware**: 动态模型选择
4. **ToolErrorMiddleware**: 工具错误处理

### 输入验证
- 检测并阻止提示注入攻击
- 识别敏感信息请求
- 过滤不当内容
- 验证工作相关性

### 输出验证
- 确保响应保持角色设定
- 防止泄露敏感信息
- 验证响应的适当性

### 安全边界
- 拒绝回答非工作相关问题
- 不处理个人隐私相关请求
- 防止参与恶意活动讨论

## 📚 API 文档

### NexusLangChainAgent

主要 Agent 类，使用 LangChain 1.0 的 `create_agent` API 构建。

#### 初始化参数

```python
NexusLangChainAgent(
    provider: str = None,              # LLM 提供商
    model: str = None,                 # 模型名称
    temperature: float = None,         # 响应随机性
    enable_safety_checks: bool = True  # 启用安全检查
)
```

#### 方法

- `process_message(user_input, context_id=None, user_preferences=None)`: 处理用户消息
- `stream_message(user_input, context_id=None, user_preferences=None)`: 流式处理消息
- `chat(message, user_preferences=None)`: 简化版对话接口
- `interactive_chat()`: 启动交互式对话
- `get_agent_info()`: 获取 Agent 信息
- `test_connection()`: 测试连接

### AgentResponse

Agent 响应数据类。

#### 属性

- `content`: 响应内容
- `success`: 是否成功
- `error`: 错误信息（如果有）
- `tokens_used`: Token 使用统计
- `duration`: 响应时间（秒）
- `context_id`: 对话 ID
- `metadata`: 额外元数据
- `tool_calls`: 工具调用记录

### 可用工具

- `lookup_company_policy(topic)`: 查询公司政策
- `get_contact_info(department)`: 获取部门联系方式
- `search_knowledge_base(query)`: 搜索知识库
- `get_onboarding_guide(step)`: 获取入职指南

## 🔧 故障排除

### 问题：API 密钥未配置

**解决方案**：确保在 `.env` 文件中配置了至少一个 API 密钥。

### 问题：连接失败

**解决方案**：
1. 检查网络连接
2. 验证 API 密钥是否正确
3. 尝试切换到其他提供商

### 问题：响应被安全检查拒绝

**解决方案**：这是正常的安全机制。确保提问与工作相关，不涉及敏感信息。

### 问题：依赖安装失败

**使用 UV 解决**：
```bash
uv sync --reinstall
```

**使用 pip 解决**：
```bash
pip install --upgrade pip
pip install -e .
```

## 🛣️ 未来计划

### Sprint 2: RAG 集成
- 文档加载和解析
- 向量数据库集成
- 知识检索能力
- 增强的上下文感知

### Sprint 3: 工具扩展
- 外部 API 集成
- 更多工具实现
- 任务自动化

### Sprint 4: Web 界面
- 用户友好的 Web UI
- 实时对话界面
- 管理后台

## 📝 开发指南

### 代码风格

项目使用 PEP 8 代码风格。建议使用 Black 进行代码格式化：

**使用 UV**：
```bash
uv run black nexus_agent/
```

**使用 pip**：
```bash
pip install black
black nexus_agent/
```

### 添加新功能

1. 在相应模块中添加代码
2. 编写单元测试
3. 更新文档
4. 提交 Pull Request

### 添加新中间件

```python
from langchain.agents.middleware import AgentMiddleware

class CustomMiddleware(AgentMiddleware):
    """自定义中间件"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("custom_middleware")
    
    def before_model(self, state, runtime) -> Optional[Dict[str, Any]]:
        # 自定义处理逻辑
        return None
```

### 添加新工具

```python
from langchain.tools import tool

@tool
def custom_tool(param: str) -> str:
    """自定义工具描述"""
    # 实现工具逻辑
    return f"处理结果: {param}"

# 添加到 NEXUS_TOOLS 列表
NEXUS_TOOLS.append(custom_tool)
```

## 📚 学习资源

- [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - 详细的项目学习指南
- [plans/langchain-1.0-syntax-guide.md](plans/langchain-1.0-syntax-guide.md) - LangChain 1.0 语法指南
- [LangChain 官方文档](https://python.langchain.com/) - LangChain 官方文档

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至项目维护者
- 加入项目讨论组

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 应用框架
- [OpenAI](https://openai.com/) - GPT 模型提供商
- [Rich](https://github.com/Textualize/rich) - 美观的终端输出库

---

**Nexus Agent** - 让新员工入职更轻松 🚀
