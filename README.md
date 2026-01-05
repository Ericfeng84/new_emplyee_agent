# Nexus Agent - 新员工入职助手

基于 LangChain 的智能对话系统，为公司新员工提供入职支持和工作协助。

## 🎯 项目概述

Nexus Agent 是一个智能助手，专门为公司新员工提供入职支持和工作协助。系统结合了对话式 AI 和检索增强生成（RAG）技术，能够基于公司文档提供准确的答案。

### 核心功能

- **Sprint 1**: 基础对话系统
  - 多模型支持（OpenAI、DeepSeek、Qwen）
  - 对话状态管理
  - 安全输入/输出验证
  - 流式响应支持

- **Sprint 2**: RAG 知识检索
  - 多格式文档加载（PDF、Markdown、Text、HTML）
  - 智能文本分割（递归和 Markdown 感知）
  - BGE 中文优化嵌入模型
  - Chroma 向量存储
  - 多种检索策略（相似性、MMR、阈值过滤）
  - RAG Agent 与检索工具集成

## 📁 项目结构

```
nexus_agent/
├── agent/                    # Agent 相关模块
│   ├── agent.py             # 主 Agent 逻辑
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
│   └── test_rag_integration.py # RAG 集成测试
└── data/                     # 数据目录
    ├── documents/          # 原始文档
    ├── processed/          # 处理后的数据
    └── chroma_db/         # 向量数据库
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

## 📖 技术文档

详细的技术文档和 Sprint 计划请查看：

- [Sprint 1 计划](plans/sprint1-prototype-plan.md)
- [Sprint 2 计划](plans/sprint2-rag-basics-plan.md)
- [LangChain 1.0 语法指南](plans/langchain-1.0-syntax-guide.md)

## 🧪 测试

项目包含全面的测试套件：

- **单元测试**: 测试各个组件的功能
- **集成测试**: 测试端到端 RAG 流程
- **手动测试**: 提供测试问题列表

运行测试：

```bash
# 所有测试
pytest

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

## 🗺️ 路线图

### Sprint 3: 工具使用 / 函数调用
- 集成外部 API 和服务
- 多步骤推理和任务执行
- 预订会议室、查询系统等工具

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
