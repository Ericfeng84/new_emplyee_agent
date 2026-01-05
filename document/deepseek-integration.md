# DeepSeek 模型集成说明

## 概述

本项目已将 DeepSeek 模型设置为默认的 LLM 提供商。DeepSeek 是一个高性能、成本效益高的中文语言模型，通过 OpenAI 兼容的 API 接口提供服务。

## 配置说明

### 1. 环境变量配置

在 `.env` 文件中配置 DeepSeek API 密钥：

```bash
# DeepSeek API Key（推荐）
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 可选：OpenAI API Key 作为备用
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. 获取 DeepSeek API Key

1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
2. 注册账号并登录
3. 进入 API Key 管理页面
4. 创建新的 API Key
5. 将 API Key 复制到 `.env` 文件中

## 使用方式

### 在 demo_rag.py 中使用

`demo_rag.py` 已配置为默认使用 DeepSeek 模型：

```python
from langchain_openai import ChatOpenAI

# 使用 DeepSeek 模型
model = ChatOpenAI(
    model="deepseek-chat",  # DeepSeek 聊天模型
    temperature=0.7,
    openai_api_key=api_key,
    base_url="https://api.deepseek.com"  # DeepSeek API 端点
)
```

### 在自定义代码中使用

```python
from langchain_openai import ChatOpenAI
import os

# 从环境变量获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 创建 DeepSeek 模型实例
model = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.7,
    openai_api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 使用模型
response = model.invoke("你好，请介绍一下你自己")
print(response.content)
```

## DeepSeek 模型选择

### 可用模型

| 模型名称 | 说明 | 适用场景 |
|---------|------|---------|
| `deepseek-chat` | DeepSeek 聊天模型 | 通用对话、问答、RAG |
| `deepseek-coder` | DeepSeek 代码模型 | 代码生成、代码解释 |

### 推荐配置

- **RAG 应用**: 使用 `deepseek-chat`
- **代码相关任务**: 使用 `deepseek-coder`
- **温度参数**: 0.7（平衡创造性和准确性）

## API 兼容性

DeepSeek API 完全兼容 OpenAI API 接口，这意味着：

1. **无缝切换**: 只需更改 `base_url` 和 `model` 参数
2. **相同接口**: 使用 LangChain 的 `ChatOpenAI` 类
3. **功能完整**: 支持流式输出、函数调用等所有 OpenAI 功能

## 成本优势

DeepSeek 相比 OpenAI GPT 模型具有显著的成本优势：

- **更低的价格**: 输入和输出成本更低
- **中文优化**: 对中文语言的理解和生成更优秀
- **高性能**: 响应速度快，质量高

## 故障排除

### 问题 1: API Key 无效

**错误信息**: `AuthenticationError`

**解决方案**:
- 检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确
- 确认 API Key 是否已激活
- 尝试重新生成 API Key

### 问题 2: 连接超时

**错误信息**: `ConnectionError` 或 `Timeout`

**解决方案**:
- 检查网络连接
- 确认 DeepSeek API 服务状态
- 考虑使用代理或 VPN

### 问题 3: 回复质量不佳

**可能原因**:
- 温度参数设置不当
- 提示词不够清晰

**解决方案**:
- 调整 `temperature` 参数（0.0-1.0）
- 优化系统提示词
- 增加上下文信息

## 回退到 OpenAI

如果需要使用 OpenAI 模型，可以：

1. 设置 `OPENAI_API_KEY` 环境变量
2. 修改模型配置：

```python
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

## 最佳实践

### 1. API Key 管理

- 不要将 API Key 提交到版本控制系统
- 使用 `.env` 文件管理敏感信息
- 定期轮换 API Key

### 2. 错误处理

```python
from langchain_openai import ChatOpenAI
from openai import AuthenticationError

try:
    model = ChatOpenAI(
        model="deepseek-chat",
        temperature=0.7,
        openai_api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    response = model.invoke("测试消息")
except AuthenticationError:
    print("API Key 无效，请检查配置")
except Exception as e:
    print(f"发生错误: {e}")
```

### 3. 性能优化

- 使用流式输出提升用户体验
- 合理设置 `max_tokens` 避免不必要的成本
- 缓存常用查询结果

## 示例代码

### 完整的 RAG 示例

```python
from langchain_openai import ChatOpenAI
from nexus_agent.rag.indexing import NexusIndexingPipeline
from nexus_agent.agent.rag_agent import NexusRAGAgentWithMemory
import os

# 配置 DeepSeek 模型
api_key = os.getenv("DEEPSEEK_API_KEY")
model = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.7,
    openai_api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 创建索引管道
pipeline = NexusIndexingPipeline(
    data_dir="nexus_agent/data/documents",
    chunk_size=1000,
    chunk_overlap=200,
    embedding_model="BAAI/bge-small-zh-v1.5"
)

# 索引文档
stats = pipeline.index_documents(verbose=True)

# 创建 RAG Agent
agent = NexusRAGAgentWithMemory(
    model=model,
    vector_store=pipeline.vector_store,
    retrieval_k=3,
    max_history_length=10
)

# 查询
response = agent.query("公司的远程办公政策是什么？")
print(response.content)
```

## 参考资源

- [DeepSeek 官方文档](https://platform.deepseek.com/docs)
- [DeepSeek API 参考](https://platform.deepseek.com/api-docs/)
- [LangChain OpenAI 集成](https://python.langchain.com/docs/integrations/chat/openai/)
- [LangChain 1.0 语法指南](../plans/langchain-1.0-syntax-guide.md)

## 更新日志

- **2026-01-05**: 将 demo_rag.py 默认模型切换为 DeepSeek
- **2026-01-05**: 更新 README.md 和 .env.example 配置
- **2026-01-05**: 添加 DeepSeek 集成文档

---

**注意**: 本文档基于 LangChain 1.0 语法编写，确保代码与最新版本兼容。
