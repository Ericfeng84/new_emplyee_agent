# Nexus Agent - 新员工入职助手

基于 LangChain 的智能对话系统，为公司新员工提供入职支持和工作协助。

## 🎯 项目概述

Nexus Agent 是一个智能助手，专门为公司新员工提供入职支持和工作协助。系统结合了对话式 AI 和检索增强生成（RAG）技术，能够基于公司文档提供准确的答案。

### 核心功能

- **Sprint 1**: 基础对话系统 ✅
  - 多模型支持（OpenAI、DeepSeek、Qwen）
  - 对话状态管理
  - 安全输入/输出验证
  - 流式响应支持

- **Sprint 2**: RAG 知识检索 ✅
  - 多格式文档加载（PDF、Markdown、Text、HTML）
  - 智能文本分割（递归和 Markdown 感知）
  - BGE 中文优化嵌入模型
  - Chroma 向量存储
  - 多种检索策略（相似性、MMR、阈值过滤）
  - RAG Agent 与检索工具集成

- **Sprint 3**: 工具调用 / 函数调用 ✅
  - 模拟企业系统 API（查人、订房、查假）
  - LangChain 1.0 工具定义和绑定
  - 自动工具选择和参数提取
  - 工具调用元数据追踪
  - 完整的测试套件（45个测试用例）

## 📁 项目结构

```
nexus_agent/
├── agent/                    # Agent 相关模块
│   ├── agent.py             # 主 Agent 逻辑
│   ├── api_tools.py        # API 工具函数 (Sprint 3)
│   ├── rag_agent.py         # RAG Agent 实现
│   ├── retrievers.py        # 检索器配置
│   ├── prompts.py           # 系统提示词
│   ├── state.py             # 对话状态管理
│   ├── tools.py             # 工具函数
│   └── middleware.py        # 中间件
├── rag/                      # RAG 相关模块
│   ├── document_loader.py   # 文档加载
│   ├── text_splitter.py     # 文本分割
│   ├── embeddings.py        # 嵌入模型
│   ├── vector_store.py      # 向量存储
│   ├── indexing.py         # 文档索引
│   └── retrieval.py        # 检索逻辑
├── config/                   # 配置管理
│   └── settings.py         # 配置设置
├── utils/                    # 工具函数
│   ├── logger.py           # 日志工具
│   ├── validators.py       # 输入/输出验证
│   └── data_preprocessing.py # 数据预处理
├── tests/                    # 测试
│   ├── test_conversation.py # 对话测试
│   ├── test_prompts.py      # 提示词测试
│   ├── test_rag.py         # RAG 组件测试
│   ├── test_rag_integration.py # RAG 集成测试
│   ├── test_api_tools.py    # API 工具单元测试 (Sprint 3)
│   └── test_tool_calling_integration.py # 工具调用集成测试 (Sprint 3)
├── data/                     # 数据目录
│   ├── documents/          # 原始文档
│   ├── processed/          # 处理后的数据
│   ├── chroma_db/         # 向量数据库
│   └── mock_data.py       # 模拟数据存储 (Sprint 3)
├── plans/                    # Sprint 计划文档
│   ├── sprint1-prototype-plan.md
│   ├── sprint2-rag-basics-plan.md
│   ├── sprint3-tool-calling-plan.md
│   └── langchain-1.0-syntax-guide.md
├── demo_rag.py              # RAG 演示脚本
├── demo_document_processing.py # 文档处理演示
└── demo_tool_calling.py     # 工具调用演示 (Sprint 3)
```

## 🚀 快速开始

### 环境要求

- Python 3.12+
- pip 或 uv 包管理器

### 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件：

```bash
# User Agent 配置（可选，用于标识请求来源）
USER_AGENT=NexusAgent/1.0 (nexus-agent-demo)

# LLM 配置
# 注意：demo_rag.py 默认使用 DeepSeek 模型
DEEPSEEK_API_KEY=your-deepseek-api-key
OPENAI_API_KEY=your-openai-api-key
QWEN_API_KEY=your-qwen-api-key

# LLM 设置
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
TEMPERATURE=0.7
```

### 运行演示

```bash
# RAG 演示
python demo_rag.py

# 文档处理演示
python demo_document_processing.py

# 交互式 RAG 演示
python demo_rag.py --interactive

# 工具调用演示 (Sprint 3)
python demo_tool_calling.py

# 交互式工具调用演示 (Sprint 3)
python demo_tool_calling.py --interactive
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest nexus_agent/tests/test_rag.py

# 运行集成测试
pytest nexus_agent/tests/test_rag_integration.py

# 查看测试覆盖率
pytest --cov=nexus_agent --cov-report=html
```

## 📚 使用指南

### 文档索引

```python
from nexus_agent.rag.indexing import NexusIndexingPipeline

# 创建索引管道
pipeline = NexusIndexingPipeline(
    data_dir="nexus_agent/data/documents",
    chunk_size=1000,
    chunk_overlap=200,
    embedding_model="BAAI/bge-small-zh-v1.5",
    persist_directory="nexus_agent/data/chroma_db"
)

# 索引文档
stats = pipeline.index_documents(verbose=True)
```

### RAG 查询

```python
from langchain_openai import ChatOpenAI
from nexus_agent.agent.rag_agent import NexusRAGAgent

# 创建模型（默认使用 DeepSeek）
model = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.7,
    base_url="https://api.deepseek.com"
)

# 创建 RAG Agent
agent = NexusRAGAgent(
    model=model,
    vector_store=pipeline.vector_store,
    retrieval_k=3
)

# 查询
response = agent.query("公司的远程办公政策是什么？")
print(response.content)
```

### 多轮对话

```python
from nexus_agent.agent.rag_agent import NexusRAGAgentWithMemory

# 创建带记忆的 Agent
agent = NexusRAGAgentWithMemory(
    model=model,
    vector_store=pipeline.vector_store,
    max_history_length=10
)

# 多轮对话
response1 = agent.query("我如何申请休假？")
response2 = agent.query("那病假呢？")

# 查看对话历史
history = agent.get_history_summary()
```

### 检索策略

```python
from nexus_agent.rag.retrieval import create_retriever

# 相似性检索
retriever = create_retriever(
    vector_store,
    search_type="similarity",
    k=3
)

# MMR 检索（多样性）
retriever = create_retriever(
    vector_store,
    search_type="mmr",
    k=3,
    fetch_k=10,
    lambda_mult=0.5
)

# 阈值检索
retriever = create_retriever(
    vector_store,
    search_type="similarity_score_threshold",
    k=5,
    score_threshold=0.7
)
```

## 🛠️ 工具调用使用 (Sprint 3)

### 查询员工信息

```python
from nexus_agent.agent.agent import NexusLangChainAgent

# 创建 Agent
agent = NexusLangChainAgent(
    provider="deepseek",
    model="deepseek-chat",
    temperature=0.7
)

# 查询员工
response = agent.process_message("张三的电话是多少？")
print(response.content)

# 查看使用的工具
if response.tool_calls:
    print(f"使用了 {len(response.tool_calls)} 个工具")
    for tool_call in response.tool_calls:
        print(f"  - {tool_call.get('name', 'Unknown')}")
```

### 预订会议室

```python
# 预订会议室
response = agent.process_message(
    "帮我预订 A1 会议室，2026-01-10 下午2点，"
    "开1小时会，我是张三，会议目的是项目讨论"
)
print(response.content)

# 查询可用会议室
response = agent.process_message(
    "明天下午2点有哪些会议室可用？"
)
print(response.content)
```

### 查询假期余额

```python
# 查询假期余额
response = agent.process_message("查一下张三的假期余额")
print(response.content)
```

### 可用的工具

- `search_employee_directory` - 搜索员工目录
- `book_meeting_room` - 预订会议室
- `query_leave_balance` - 查询假期余额
- `get_available_meeting_rooms` - 查询可用会议室
- `retrieve_context` - 检索知识库

## 🔧 配置说明

### LLM 配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `llm_provider` | LLM 提供商 | `deepseek` |
| `llm_model` | 模型名称 | `deepseek-chat` |
| `temperature` | 温度参数 | `0.7` |

### RAG 配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `data_directory` | 文档目录 | `nexus_agent/data/documents` |
| `chunk_size` | 分块大小 | `1000` |
| `chunk_overlap` | 分块重叠 | `200` |
| `embedding_model` | 嵌入模型 | `BAAI/bge-small-zh-v1.5` |
| `retrieval_k` | 检索数量 | `3` |

### 工具调用配置 (Sprint 3)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `enable_tool_calling` | 启用工具调用功能 | `True` |
| `tool_calling_timeout` | 工具调用超时时间（秒） | `30.0` |
| `max_tool_calls_per_query` | 每次查询最多调用工具次数 | `5` |

## 📖 技术文档

详细的技术文档和 Sprint 计划请查看：

- [Sprint 1 计划](plans/sprint1-prototype-plan.md)
- [Sprint 2 计划](plans/sprint2-rag-basics-plan.md)
- [Sprint 3 计划 - 工具调用 ✅ 已完成](plans/sprint3-tool-calling-plan.md)
- [LangChain 1.0 语法指南](plans/langchain-1.0-syntax-guide.md)

## 🧪 测试

项目包含全面的测试套件：

- **单元测试**: 测试各个组件的功能
  - 对话测试
  - RAG 组件测试
  - API 工具测试 (Sprint 3) - 26个测试用例
- **集成测试**: 测试端到端流程
  - RAG 集成测试
  - 工具调用集成测试 (Sprint 3) - 19个测试用例
- **手动测试**: 提供测试问题列表

### 测试覆盖

- **Sprint 1 & 2**: 对话和 RAG 功能
- **Sprint 3**: 工具调用功能
  - 单元测试：26个测试用例
  - 集成测试：19个测试用例
  - 总计：45个测试用例
  - 覆盖率：> 90%

运行测试：

```bash
# 所有测试
pytest

# Sprint 3 工具调用测试
pytest nexus_agent/tests/test_api_tools.py
pytest nexus_agent/tests/test_tool_calling_integration.py

# 带覆盖率
pytest --cov=nexus_agent --cov-report=html
```

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 开发规范

- 使用 LangChain 1.0 语法
- 代码注释详细，方便学习
- 遵循 PEP 8 代码风格
- 编写测试覆盖新功能
- 更新相关文档

## 🏆 Sprint 3 成就

Sprint 3 已成功完成！以下是主要成就：

### 核心功能
- ✅ 实现了4个 API 工具函数（查人、订房、查假、查可用会议室）
- ✅ 创建了3个模拟企业系统（员工目录、会议室预订、假期管理）
- ✅ 集成到 LangChain 1.0 Agent 架构
- ✅ 实现了自动工具选择和参数提取
- ✅ 添加了完整的工具调用元数据追踪

### 测试成果
- ✅ 45个测试用例（26个单元测试 + 19个集成测试）
- ✅ 测试覆盖率 > 90%
- ✅ 包含错误处理、性能测试、上下文集成测试

### 代码质量
- ✅ 遵循 LangChain 1.0 最佳实践
- ✅ 详细的中文注释和文档
- ✅ 完整的类型提示
- ✅ 良好的错误处理和用户友好的提示

### 文档和演示
- ✅ 完整的 Sprint 3 计划文档
- ✅ 自动化和交互式演示脚本
- ✅ 使用指南和代码示例

**完成日期：** 2026-01-05
**状态：** ✅ 成功完成

## 🗺️ 路线图

### ✅ Sprint 3: 工具使用 / 函数调用 - 已完成
- 集成外部 API 和服务
- 多步骤推理和任务执行
- 预订会议室、查询系统等工具
- 45个测试用例，覆盖率 > 90%

### Sprint 4: 高级功能
- 多模态支持（图像、音频）
- 知识图谱集成
- 个性化推荐

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 应用框架
- [BGE](https://github.com/FlagOpen/FlagEmbedding) - 优秀的中文嵌入模型
- [Chroma](https://www.trychroma.com/) - 开源向量数据库

## 📞 联系方式

如有问题或建议，请：

- 提交 Issue
- 发送邮件至：support@company.com
- 查看 [项目文档](document/)

---

**Nexus Agent** - 帮助新员工快速适应工作环境，提高工作效率 🚀
