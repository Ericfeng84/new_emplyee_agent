# Nexus Agent - 企业级 AI 开发实战课程

## 🌟 项目愿景：打造生产级智能入职助手

**项目代号:** "Nexus"
**应用场景:** 部署在企业 IM (钉钉/飞书/Slack) 中的智能 Agent，帮助新员工快速适应工作环境
**核心目标:** 拒绝"Demo 玩具"，掌握从 Prompt 到生产级 Agent 的全生命周期开发

---

## 📊 项目现状

### ✅ 已完成 Sprint (截至 2026-01-09)

| Sprint | 功能模块 | 完成度 | 状态 |
|--------|---------|--------|------|
| Sprint 1 | 基础对话系统 | 100% | ✅ 已完成 |
| Sprint 2 | RAG 知识检索 | 100% | ✅ 已完成 |
| Sprint 3 | 工具调用系统 | 100% | ✅ 已完成 |
| Sprint 4 | Redis 记忆管理 | 100% | ✅ 已完成 |
| Sprint 5 | FastAPI 服务 | 100% | ✅ 已完成 |
| Sprint 6 | React 前端开发 | 100% | ✅ 已完成 |

### 🎯 核心成果

- **45+ 测试用例**，覆盖率 > 90%
- **6 个 Sprint** 完整实现
- **生产级代码**，遵循 LangChain 1.0 最佳实践
- **完整的前后端分离架构**
- **详细的中文注释和文档**

---

## 🎯 课程学习目标

通过本实战课程，你将掌握：

### 1. LLM 基础与工程化
- 深入理解 Prompt 工程与系统提示词设计
- 掌握无状态 API 的并发控制与流式响应
- 实现多模型支持（OpenAI、DeepSeek、Qwen）
- 理解温度参数、上下文窗口等核心概念

### 2. RAG 架构实战
- 解决私有数据幻觉问题
- 掌握高级检索策略（相似度、MMR、阈值过滤）
- 实现文档加载、分块、嵌入、索引完整流程
- 使用 BGE 中文优化嵌入模型
- Chroma 向量数据库集成与管理

### 3. Agent 设计模式
- LangChain 1.0 的 `create_agent` API 使用
- Function Calling / Tool Calling 实战
- ReAct 推理模式
- 中间件架构（Middleware Pattern）
- 多工具协同与自动决策

### 4. AI 工程化 (LLMOps)
- Redis 会话持久化与多用户隔离
- 智能上下文压缩与 Token 管理
- 统一错误处理与日志追踪
- 安全验证与输入/输出护栏
- 完整的测试策略（单元测试、集成测试）

### 5. 全栈开发能力
- FastAPI 后端服务开发
- OpenAI 兼容的 RESTful API 设计
- React 18 + Vite 前端开发
- WebSocket/SSE 流式响应
- 前后端联调与 CORS 处理

**适用人群:** Python 开发者，希望转型 AI 工程师

---

## 🛠️ 技术栈清单 (The Toolkit)

### 后端技术栈

| 技术类别 | 技术选型 | 版本/说明 |
|---------|---------|----------|
| **编程语言** | Python | 3.10+ (Type Hints 强类型) |
| **LLM 框架** | LangChain | 1.0 (Core/Community) |
| **模型服务** | OpenAI / DeepSeek / Qwen | GPT-4o, deepseek-chat, qwen-turbo |
| **向量数据库** | Chroma | 本地持久化存储 |
| **嵌入模型** | BGE (BAAI) | bge-small-zh-v1.5 (中文优化) |
| **Web 框架** | FastAPI | Async I/O, 自动文档生成 |
| **会话存储** | Redis | 多用户会话隔离 |
| **包管理** | UV | 快速依赖管理 |
| **测试框架** | pytest | 单元测试、集成测试 |

### 前端技术栈

| 技术类别 | 技术选型 | 版本/说明 |
|---------|---------|----------|
| **框架** | React | 18+ (Hooks) |
| **构建工具** | Vite | 快速开发服务器 |
| **HTTP 客户端** | Axios | API 请求与错误处理 |
| **状态管理** | React Hooks + localStorage | 会话持久化 |
| **样式方案** | CSS Modules | 样式隔离 |
| **图标库** | Lucide React | 现代图标 |
| **Markdown** | react-markdown | Markdown 渲染 |

### 开发工具

| 工具类别 | 工具选型 | 用途 |
|---------|---------|------|
| **代码编辑器** | VS Code | 推荐使用 |
| **API 测试** | curl / Postman | API 调试 |
| **数据库管理** | redis-cli | Redis 数据查看 |
| **版本控制** | Git | 代码管理 |

---

## 🚀 实战路线图 (Curriculum Roadmap)

### 第一阶段：核心基础 (Phase 1: Foundation)

#### Sprint 1: 基础对话系统 ✅

**学习目标:**
- 理解 LangChain 1.0 的核心概念
- 掌握 Prompt 工程与系统提示词设计
- 实现多模型支持与动态模型选择
- 构建安全验证中间件

**核心模块:**

##### 模块 1: 大脑 (LLM Fundamentals)
*   **核心概念**: 
    - 上下文窗口 (Context Window)
    - 温度参数 (Temperature)
    - 角色扮演 (Persona)
    - LangChain 1.0 的 `create_agent` API
*   **实战任务**:
    - 搭建基础 LLM 客户端（支持 OpenAI、DeepSeek、Qwen）
    - 设计 "HR 贴心助手" 的 System Prompt
    - 实现动态模型选择中间件
    - *挑战*: 尝试 "Prompt 注入" 攻击自己的 Agent
*   **💻 代码示例**:
    ```python
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_agent
    from langchain.agents import AgentState
    from langchain_core.prompts import ChatPromptTemplate
    from pydantic import BaseModel, Field
    from typing import Optional, Dict, Any

    # 1. 定义扩展的状态
    class NexusAgentState(AgentState):
        user_id: Optional[str] = None
        session_id: Optional[str] = None
        user_preferences: Dict[str, Any] = {}

    # 2. 初始化模型
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0.7,
        streaming=True,
        base_url="https://api.deepseek.com"
    )

    # 3. 定义系统提示词
    SYSTEM_PROMPT = """你是 Nexus，一个热情的 HR 助手，专门帮助新员工。
    
    你的职责：
    - 回答关于入职流程、公司政策的问题
    - 提供工作相关的帮助和建议
    - 保持友好、专业的态度
    
    限制：
    - 只回答与工作相关的问题
    - 不提供个人建议或非工作话题
    """

    # 4. 创建 Agent（LangChain 1.0 语法）
    agent = create_agent(
        model=llm,
        tools=[],
        state_schema=NexusAgentState,
        system_prompt=SYSTEM_PROMPT
    )

    # 5. 调用
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": "我的年假有多少天？"}
        ]
    })
    print(response["messages"][-1].content)
    ```

##### 模块 2: 中间件架构 (Middleware Pattern)
*   **核心概念**: 
    - LangChain 1.0 中间件机制
    - 责任链模式 (Chain of Responsibility)
    - before_model / after_model 钩子
*   **实战任务**:
    - 实现安全验证中间件（输入/输出检查）
    - 实现动态模型选择中间件
    - 实现动态提示词生成中间件
    - 实现工具错误处理中间件
*   **💻 代码示例**:
    ```python
    from langchain.agents.middleware import AgentMiddleware
    from langchain.agents.middleware import wrap_model_call

    class SafetyMiddleware(AgentMiddleware):
        """安全验证中间件"""
        
        def __init__(self):
            super().__init__()
            self.logger = get_logger("safety")
        
        @wrap_model_call
        def before_model(self, state: NexusAgentState, runtime):
            """模型调用前验证输入"""
            user_input = state["messages"][-1].content
            
            # 检查提示注入
            if self._is_prompt_injection(user_input):
                self.logger.log_safety_violation(
                    "prompt_injection",
                    user_input,
                    "block"
                )
                return {
                    "skip_model": True,
                    "safety_violation": True,
                    "response": "抱歉，我无法处理这个请求。"
                }
            
            return None
        
        def _is_prompt_injection(self, text: str) -> bool:
            """检测提示注入"""
            patterns = [
                r"(?i)(ignore|forget|disregard).*previous.*instruction",
                r"(?i)(override|bypass).*system.*prompt"
            ]
            return any(re.search(p, text) for p in patterns)
    
    # 创建 Agent 时添加中间件
    agent = create_agent(
        model=llm,
        tools=[],
        state_schema=NexusAgentState,
        middleware=[SafetyMiddleware()],
        system_prompt=SYSTEM_PROMPT
    )
    ```

##### 模块 3: 安全验证系统 (Safety & Validation)
*   **核心概念**: 
    - 输入验证（提示注入、敏感信息）
    - 输出验证（角色保持、敏感内容）
    - 正则表达式模式匹配
*   **实战任务**:
    - 实现输入验证器（InputValidator）
    - 实现输出验证器（OutputValidator）
    - 构建验证规则库
    - 集成到中间件链
*   **💻 代码示例**:
    ```python
    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class ValidationResult:
        is_valid: bool
        reason: str
        action: str  # allow/block/modify

    class InputValidator:
        """输入验证器"""
        
        def validate(self, text: str) -> ValidationResult:
            # 1. 检查空输入
            if not text or not text.strip():
                return ValidationResult(
                    is_valid=False,
                    reason="输入为空",
                    action="block"
                )
            
            # 2. 检查提示注入
            if self._check_prompt_injection(text):
                return ValidationResult(
                    is_valid=False,
                    reason="检测到提示注入攻击",
                    action="block"
                )
            
            # 3. 检查敏感信息
            if self._check_sensitive_info(text):
                return ValidationResult(
                    is_valid=False,
                    reason="包含敏感信息",
                    action="block"
                )
            
            # 4. 检查工作相关性
            if not self._check_work_related(text):
                return ValidationResult(
                    is_valid=False,
                    reason="非工作相关问题",
                    action="block"
                )
            
            return ValidationResult(
                is_valid=True,
                reason="验证通过",
                action="allow"
            )
    ```

---

#### Sprint 2: RAG 知识检索系统 ✅

**学习目标:**
- 理解 RAG（检索增强生成）架构
- 掌握文档加载、分块、嵌入、索引流程
- 实现多种检索策略
- 使用 BGE 中文嵌入模型

**核心模块:**

##### 模块 1: 文档处理管道 (Document Processing)
*   **核心概念**: 
    - 文档加载器（Document Loaders）
    - 文本分割器（Text Splitters）
    - 递归分割 vs Markdown 感知分割
    - 元数据增强
*   **实战任务**:
    - 实现多格式文档加载（PDF、Markdown、HTML、Text）
    - 实现智能文本分割（递归和 Markdown 感知）
    - 增强文档元数据（来源、类型、大小）
    - 构建文档统计功能
*   **💻 代码示例**:
    ```python
    from langchain_community.document_loaders import (
        PyPDFLoader, TextLoader, WebBaseLoader
    )
    from langchain_text_splitters import (
        RecursiveCharacterTextSplitter,
        MarkdownTextSplitter
    )

    class NexusDocumentLoader:
        """多格式文档加载器"""
        
        def __init__(self, data_dir: str = "nexus_agent/data/documents"):
            self.data_dir = data_dir
            self.loaders = {
                '.pdf': PyPDFLoader,
                '.txt': TextLoader,
                '.md': TextLoader,
                '.html': WebBaseLoader
            }
        
        def load_documents(self, file_paths=None):
            """加载文档"""
            docs = []
            
            for file_path in self._get_files(file_paths):
                # 根据扩展名选择加载器
                ext = os.path.splitext(file_path)[1].lower()
                loader_class = self.loaders.get(ext)
                
                if loader_class:
                    loader = loader_class(file_path)
                    loaded_docs = loader.load()
                    
                    # 增强元数据
                    for doc in loaded_docs:
                        doc.metadata.update({
                            'source': file_path,
                            'file_type': ext,
                            'file_name': os.path.basename(file_path),
                            'file_size': os.path.getsize(file_path)
                        })
                    
                    docs.extend(loaded_docs)
            
            return docs

    # 1. 加载文档
    loader = NexusDocumentLoader()
    docs = loader.load_documents()

    # 2. 分割文档（递归分割）
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n\n", "\n\n", "\n", " ", ""]
    )
    splits = splitter.split_documents(docs)

    # 3. 分割文档（Markdown 感知）
    md_splitter = MarkdownTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    md_splits = md_splitter.split_documents(docs)
    ```

##### 模块 2: 嵌入模型 (Embeddings)
*   **核心概念**: 
    - 向量嵌入（Vector Embeddings）
    - BGE 中文嵌入模型
    - 余弦相似度（Cosine Similarity）
    - 嵌入归一化
*   **实战任务**:
    - 集成 BGE 中文嵌入模型
    - 实现单个查询和批量文档嵌入
    - 计算余弦相似度
    - 实现嵌入缓存
*   **💻 代码示例**:
    ```python
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from typing import List, Optional

    class NexusEmbeddings:
        """BGE 中文嵌入模型"""
        
        def __init__(
            self,
            model_name: str = "BAAI/bge-small-zh-v1.5",
            device: str = "cpu",
            normalize_embeddings: bool = True
        ):
            self.model = SentenceTransformer(model_name, device=device)
            self.normalize_embeddings = normalize_embeddings
            self.cache = {}
        
        def embed_query(self, text: str) -> List[float]:
            """嵌入单个查询"""
            # 检查缓存
            if text in self.cache:
                return self.cache[text]
            
            # 生成嵌入
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=self.normalize_embeddings
            )
            
            # 缓存结果
            self.cache[text] = embedding.tolist()
            return embedding.tolist()
        
        def embed_documents(self, texts: List[str]) -> List[List[float]]:
            """批量嵌入文档"""
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=self.normalize_embeddings
            )
            return embeddings.tolist()
        
        def compute_similarity(
            self,
            embedding1: List[float],
            embedding2: List[float]
        ) -> float:
            """计算余弦相似度"""
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # 点积
            dot_product = np.dot(vec1, vec2)
            
            # 欧几里得范数
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            # 余弦相似度
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)

    # 使用示例
    embeddings = NexusEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        device="cpu",
        normalize_embeddings=True
    )

    # 嵌入查询
    query_embedding = embeddings.embed_query("公司的远程办公政策是什么？")
    print(f"嵌入维度: {len(query_embedding)}")

    # 嵌入文档
    docs = ["公司政策", "IT支持", "员工福利"]
    doc_embeddings = embeddings.embed_documents(docs)

    # 计算相似度
    similarity = embeddings.compute_similarity(
        query_embedding,
        doc_embeddings[0]
    )
    print(f"相似度: {similarity:.4f}")
    ```

##### 模块 3: 向量存储与检索 (Vector Store & Retrieval)
*   **核心概念**: 
    - Chroma 向量数据库
    - 相似度搜索（Similarity Search）
    - MMR 搜索（最大边际相关性）
    - 阈值过滤（Threshold Filtering）
*   **实战任务**:
    - 集成 Chroma 向量数据库
    - 实现持久化存储
    - 实现多种检索策略
    - 实现元数据过滤
*   **💻 代码示例**:
    ```python
    from langchain_chroma import Chroma
    from langchain_core.documents import Document

    class NexusVectorStore:
        """Chroma 向量存储管理器"""
        
        def __init__(
            self,
            embeddings,
            collection_name: str = "nexus_knowledge_base",
            persist_directory: str = "nexus_agent/data/chroma_db"
        ):
            self.embeddings = embeddings
            self.collection_name = collection_name
            self.persist_directory = persist_directory
            
            # 初始化向量存储
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=persist_directory
            )
        
        def add_documents(self, documents: List[Document]) -> List[str]:
            """添加文档到向量存储"""
            return self.vectorstore.add_documents(documents)
        
        def similarity_search(
            self,
            query: str,
            k: int = 3,
            filter: Optional[dict] = None
        ) -> List[Document]:
            """相似度搜索"""
            return self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
        
        def similarity_search_with_score(
            self,
            query: str,
            k: int = 3
        ) -> List[tuple]:
            """带分数的相似度搜索"""
            return self.vectorstore.similarity_search_with_score(
                query=query,
                k=k
            )
        
        def max_marginal_relevance_search(
            self,
            query: str,
            k: int = 3,
            fetch_k: int = 10,
            lambda_mult: float = 0.5
        ) -> List[Document]:
            """MMR 搜索（平衡相关性和多样性）"""
            return self.vectorstore.max_marginal_relevance_search(
                query=query,
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult
            )

    # 使用示例
    vector_store = NexusVectorStore(embeddings=embeddings)

    # 添加文档
    docs = [
        Document(page_content="公司远程办公政策...", metadata={"source": "policy.md"}),
        Document(page_content="IT支持VPN配置...", metadata={"source": "it.md"}),
    ]
    vector_store.add_documents(docs)

    # 相似度搜索
    results = vector_store.similarity_search("远程办公", k=3)

    # 带分数的搜索
    results_with_scores = vector_store.similarity_search_with_score("远程办公", k=3)
    for doc, score in results_with_scores:
        print(f"分数: {score:.4f}")
        print(f"内容: {doc.page_content[:100]}...")

    # MMR 搜索
    mmr_results = vector_store.max_marginal_relevance_search(
        "远程办公",
        k=3,
        fetch_k=10,
        lambda_mult=0.5
    )
    ```

##### 模块 4: RAG Agent 实现 (RAG Agent)
*   **核心概念**: 
    - 检索增强生成（RAG）
    - 检索工具（Retrieval Tool）
    - 上下文注入
    - 来源引用
*   **实战任务**:
    - 实现检索工具
    - 构建 RAG Agent
    - 实现带记忆的 RAG Agent
    - 优化检索参数
*   **💻 代码示例**:
    ```python
    from langchain.tools import tool
    from langchain.agents import create_agent

    class NexusRAGAgent:
        """RAG 启用的 Nexus Agent"""
        
        def __init__(
            self,
            model,
            vector_store,
            system_prompt: Optional[str] = None,
            retrieval_k: int = 3
        ):
            self.model = model
            self.vector_store = vector_store
            self.retrieval_k = retrieval_k
            
            # 定义检索工具
            @tool
            def retrieve_context(query: str) -> str:
                """从公司知识库中检索相关信息
                
                Args:
                    query: 用户查询的问题
                
                Returns:
                    检索到的相关文档内容
                """
                # 执行相似度搜索
                retrieved_docs = vector_store.similarity_search(
                    query,
                    k=retrieval_k
                )
                
                # 序列化文档
                context_parts = []
                for i, doc in enumerate(retrieved_docs, 1):
                    source = doc.metadata.get('source', '未知来源')
                    content = doc.page_content
                    context_parts.append(
                        f"【来源 {i}】\n"
                        f"文件: {source}\n"
                        f"内容: {content}"
                    )
                
                return "\n\n".join(context_parts)
            
            # 创建 Agent
            self.agent = create_agent(
                model=model,
                tools=[retrieve_context],
                state_schema=NexusAgentState,
                system_prompt=system_prompt or self._get_default_prompt()
            )
        
        def query(self, user_input: str) -> AgentResponse:
            """处理用户查询"""
            start_time = time.time()
            
            try:
                result = self.agent.invoke({
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                })
                
                response_content = result["messages"][-1].content
                duration = time.time() - start_time
                
                return AgentResponse(
                    content=response_content,
                    success=True,
                    duration=duration,
                    metadata={"retrieval_k": self.retrieval_k}
                )
            
            except Exception as e:
                return AgentResponse(
                    content="",
                    success=False,
                    error=str(e)
                )
        
        def _get_default_prompt(self) -> str:
            """获取默认系统提示词"""
            return """你是 Nexus，一个智能入职助手，基于公司知识库回答问题。

    使用指南：
    1. 使用 retrieve_context 工具检索相关信息
    2. 基于检索到的上下文回答问题
    3. 在回答中引用来源
    4. 如果知识库中没有相关信息，诚实告知

    回答风格：
    - 专业、友好、准确
    - 提供具体、可操作的建议
    - 引用相关文档来源
    """

    # 使用示例
    model = ChatOpenAI(model="deepseek-chat", temperature=0.7)
    rag_agent = NexusRAGAgent(
        model=model,
        vector_store=vector_store,
        retrieval_k=3
    )

    # 查询
    response = rag_agent.query("公司的远程办公政策是什么？")
    print(response.content)
    ```

---

#### Sprint 3: 工具调用系统 ✅

**学习目标:**
- 掌握 LangChain 1.0 的工具调用机制
- 实现企业系统 API 模拟
- 实现自动工具选择与参数提取
- 构建完整的测试套件

**核心模块:**

##### 模块 1: 工具定义 (Tool Definition)
*   **核心概念**: 
    - LangChain 1.0 `@tool` 装饰器
    - JSON Schema
    - 函数调用（Function Calling）
    - 工具元数据
*   **实战任务**:
    - 定义查人工具（search_employee）
    - 定义订房工具（book_meeting_room）
    - 定义查假工具（query_leave_balance）
    - 定义查可用会议室工具（get_available_meeting_rooms）
*   **💻 代码示例**:
    ```python
    from langchain.tools import tool
    from typing import Optional

    # 1. 查询员工目录
    @tool
    def search_employee_directory(name: str) -> str:
        """根据姓名查询员工的部门和邮箱
        
        Args:
            name: 员工姓名
        
        Returns:
            员工信息（部门、邮箱、电话）
        """
        # 模拟数据库查询
        employee_db = {
            "张三": {
                "department": "工程部",
                "email": "zhangsan@nexus.com",
                "phone": "13800138000"
            },
            "李四": {
                "department": "产品部",
                "email": "lisi@nexus.com",
                "phone": "13900139000"
            }
        }
        
        employee = employee_db.get(name)
        if employee:
            return f"{name} 是 {employee['department']} 的员工，邮箱 {employee['email']}"
        else:
            return f"未找到员工 {name} 的信息"
    
    # 2. 预订会议室
    @tool
    def book_meeting_room(
        room: str,
        date: str,
        time: str,
        duration: int,
        booker: str,
        purpose: str
    ) -> str:
        """预订会议室
        
        Args:
            room: 会议室名称（如 A1, B2）
            date: 日期（格式：YYYY-MM-DD）
            time: 开始时间（格式：HH:MM）
            duration: 预订时长（小时）
            booker: 预订人姓名
            purpose: 会议目的
        
        Returns:
            预订结果
        """
        # 模拟预订逻辑
        return f"会议室 {room} 已预订：{date} {time}，时长 {duration} 小时，预订人：{booker}，目的：{purpose}"
    
    # 3. 查询假期余额
    @tool
    def query_leave_balance(name: str) -> str:
        """查询员工的假期余额
        
        Args:
            name: 员工姓名
        
        Returns:
            假期余额信息
        """
        # 模拟数据库查询
        leave_db = {
            "张三": {
                "annual_leave": 10,
                "sick_leave": 5,
                "personal_leave": 3
            },
            "李四": {
                "annual_leave": 15,
                "sick_leave": 3,
                "personal_leave": 2
            }
        }
        
        balance = leave_db.get(name)
        if balance:
            return f"{name} 的假期余额：年假 {balance['annual_leave']} 天，病假 {balance['sick_leave']} 天，事假 {balance['personal_leave']} 天"
        else:
            return f"未找到员工 {name} 的假期信息"
    
    # 4. 查询可用会议室
    @tool
    def get_available_meeting_rooms(date: str, time: str) -> str:
        """查询指定日期时间的可用会议室
        
        Args:
            date: 日期（格式：YYYY-MM-DD）
            time: 时间（格式：HH:MM）
        
        Returns:
            可用会议室列表
        """
        # 模拟查询逻辑
        all_rooms = ["A1", "A2", "B1", "B2", "C1"]
        booked_rooms = ["A1", "B2"]  # 模拟已预订
        
        available = [room for room in all_rooms if room not in booked_rooms]
        return f"{date} {time} 可用的会议室：{', '.join(available)}"
    
    # 工具列表
    NEXUS_TOOLS = [
        search_employee_directory,
        book_meeting_room,
        query_leave_balance,
        get_available_meeting_rooms
    ]
    ```

##### 模块 2: 工具绑定与调用 (Tool Binding & Calling)
*   **核心概念**: 
    - `bind_tools()` 方法
    - 自动工具选择
    - 参数提取
    - 工具调用追踪
*   **实战任务**:
    - 将工具绑定到 LLM
    - 实现自动工具选择逻辑
    - 追踪工具调用次数和执行时间
    - 处理工具调用错误
*   **💻 代码示例**:
    ```python
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_agent
    from typing import Dict, List, Optional
    import time

    class NexusLangChainAgent:
        """带工具调用的 Nexus Agent"""
        
        def __init__(
            self,
            provider: str = "deepseek",
            model: str = "deepseek-chat",
            temperature: float = 0.7,
            tools: Optional[List] = None
        ):
            self.provider = provider
            self.model = model
            self.temperature = temperature
            self.tools = tools or NEXUS_TOOLS
            
            # 初始化模型
            self.base_model = self._get_model()
            
            # 创建 Agent
            self.agent = create_agent(
                model=self.base_model,
                tools=self.tools,
                state_schema=NexusAgentState,
                system_prompt=self._get_system_prompt()
            )
            
            # 工具调用统计
            self.tool_call_stats = {}
        
        def _get_model(self) -> ChatOpenAI:
            """获取模型"""
            if self.provider == "deepseek":
                return ChatOpenAI(
                    model=self.model,
                    temperature=self.temperature,
                    base_url="https://api.deepseek.com"
                )
            elif self.provider == "openai":
                return ChatOpenAI(
                    model=self.model,
                    temperature=self.temperature
                )
            # ... 其他提供商
        
        def process_message(self, message: str) -> AgentResponse:
            """处理用户消息"""
            start_time = time.time()
            tool_calls = []
            
            try:
                # 调用 Agent
                result = self.agent.invoke({
                    "messages": [
                        {"role": "user", "content": message}
                    ]
                })
                
                # 提取工具调用信息
                response_content = result["messages"][-1].content
                
                # 检查是否有工具调用
                for msg in result["messages"]:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            tool_calls.append({
                                'name': tool_call['name'],
                                'args': tool_call['args'],
                                'id': tool_call['id']
                            })
                            
                            # 更新统计
                            self._update_tool_stats(tool_call['name'])
                
                duration = time.time() - start_time
                
                return AgentResponse(
                    content=response_content,
                    success=True,
                    duration=duration,
                    tool_calls=tool_calls,
                    metadata={
                        'tool_calls_count': len(tool_calls),
                        'tool_call_stats': self.tool_call_stats
                    }
                )
            
            except Exception as e:
                return AgentResponse(
                    content="",
                    success=False,
                    error=str(e),
                    duration=time.time() - start_time
                )
        
        def _update_tool_stats(self, tool_name: str):
            """更新工具调用统计"""
            if tool_name not in self.tool_call_stats:
                self.tool_call_stats[tool_name] = {
                    'count': 0,
                    'last_called': None
                }
            
            self.tool_call_stats[tool_name]['count'] += 1
            self.tool_call_stats[tool_name]['last_called'] = time.time()
        
        def _get_system_prompt(self) -> str:
            """获取系统提示词"""
            return """你是 Nexus，一个智能入职助手。

    可用工具：
    - search_employee_directory: 查询员工信息
    - book_meeting_room: 预订会议室
    - query_leave_balance: 查询假期余额
    - get_available_meeting_rooms: 查询可用会议室

    使用指南：
    1. 根据用户需求自动选择合适的工具
    2. 从用户输入中提取工具所需的参数
    3. 调用工具并获取结果
    4. 基于工具结果生成友好的回答
    """

    # 使用示例
    agent = NexusLangChainAgent(
        provider="deepseek",
        model="deepseek-chat",
        temperature=0.7
    )

    # 查询员工
    response = agent.process_message("张三的电话是多少？")
    print(response.content)
    if response.tool_calls:
        print(f"使用了 {len(response.tool_calls)} 个工具")
        for tool_call in response.tool_calls:
            print(f"  - {tool_call['name']}")
    
    # 预订会议室
    response = agent.process_message(
        "帮我预订 A1 会议室，2026-01-10 下午2点，"
        "开1小时会，我是张三，会议目的是项目讨论"
    )
    print(response.content)
    ```

##### 模块 3: 测试套件 (Test Suite)
*   **核心概念**: 
    - 单元测试（Unit Tests）
    - 集成测试（Integration Tests）
    - pytest 框架
    - Mock 和 Fixture
*   **实战任务**:
    - 编写工具单元测试（26 个测试用例）
    - 编写工具调用集成测试（19 个测试用例）
    - 实现测试覆盖率 > 90%
    - 编写性能测试
*   **💻 代码示例**:
    ```python
    import pytest
    from nexus_agent.agent.api_tools import (
        search_employee_directory,
        book_meeting_room,
        query_leave_balance,
        get_available_meeting_rooms
    )

    class TestEmployeeDirectory:
        """测试员工目录工具"""
        
        def test_search_existing_employee(self):
            """测试查询存在的员工"""
            result = search_employee_directory.invoke({"name": "张三"})
            assert "工程部" in result
            assert "zhangsan@nexus.com" in result
        
        def test_search_nonexistent_employee(self):
            """测试查询不存在的员工"""
            result = search_employee_directory.invoke({"name": "王五"})
            assert "未找到" in result
        
        def test_search_empty_name(self):
            """测试空姓名"""
            with pytest.raises(Exception):
                search_employee_directory.invoke({"name": ""})
        
        def test_search_special_characters(self):
            """测试特殊字符"""
            result = search_employee_directory.invoke({"name": "张三@#$%"})
            # 应该返回未找到或错误
            assert "未找到" in result or "错误" in result

    class TestMeetingRoom:
        """测试会议室工具"""
        
        def test_book_meeting_room_success(self):
            """测试成功预订会议室"""
            result = book_meeting_room.invoke({
                "room": "A1",
                "date": "2026-01-10",
                "time": "14:00",
                "duration": 1,
                "booker": "张三",
                "purpose": "项目讨论"
            })
            assert "已预订" in result
            assert "A1" in result
        
        def test_book_meeting_room_invalid_date(self):
            """测试无效日期"""
            with pytest.raises(Exception):
                book_meeting_room.invoke({
                    "room": "A1",
                    "date": "2026-13-32",  # 无效日期
                    "time": "14:00",
                    "duration": 1,
                    "booker": "张三",
                    "purpose": "项目讨论"
                })
        
        def test_get_available_rooms(self):
            """测试查询可用会议室"""
            result = get_available_meeting_rooms.invoke({
                "date": "2026-01-10",
                "time": "14:00"
            })
            assert "可用" in result
            assert "A1" in result or "A2" in result

    class TestToolCallingIntegration:
        """测试工具调用集成"""
        
        def test_employee_query_with_tool_calling(self, agent):
            """测试员工查询的工具调用"""
            response = agent.process_message("张三的电话是多少？")
            
            assert response.success
            assert len(response.tool_calls) > 0
            assert response.tool_calls[0]['name'] == 'search_employee_directory'
        
        def test_meeting_booking_with_tool_calling(self, agent):
            """测试会议室预订的工具调用"""
            response = agent.process_message(
                "帮我预订 A1 会议室，2026-01-10 下午2点，"
                "开1小时会，我是张三"
            )
            
            assert response.success
            assert len(response.tool_calls) > 0
            assert response.tool_calls[0]['name'] == 'book_meeting_room'
        
        def test_multiple_tool_calls(self, agent):
            """测试多次工具调用"""
            response1 = agent.process_message("查一下张三的信息")
            response2 = agent.process_message("再查一下李四的信息")
            
            assert response1.success
            assert response2.success
            assert len(response1.tool_calls) > 0
            assert len(response2.tool_calls) > 0

    # 运行测试
    # pytest nexus_agent/tests/test_api_tools.py -v
    # pytest nexus_agent/tests/test_tool_calling_integration.py -v
    # pytest --cov=nexus_agent --cov-report=html
    ```

---

#### Sprint 4: Redis 记忆管理 ✅

**学习目标:**
- 理解会话持久化的重要性
- 掌握 Redis 客户端封装
- 实现智能上下文压缩
- 实现多用户会话隔离

**核心模块:**

##### 模块 1: Redis 客户端封装 (Redis Client)
*   **核心概念**: 
    - Redis 数据结构（String、Hash、List）
    - 连接池管理
    - 错误处理与重试
    - 数据序列化（JSON）
*   **实战任务**:
    - 封装 Redis 客户端
    - 实现连接池管理
    - 实现错误处理与重试机制
    - 实现数据序列化/反序列化
*   **💻 代码示例**:
    ```python
    import redis
    from redis.connection import ConnectionPool
    from typing import Optional, Any, Dict
    import json
    import logging

    class RedisClient:
        """Redis 客户端封装"""
        
        def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0,
            password: Optional[str] = None,
            max_connections: int = 10
        ):
            self.host = host
            self.port = port
            self.db = db
            self.password = password
            
            # 创建连接池
            self.pool = ConnectionPool(
                host=host,
                port=port,
                db=db,
                password=password,
                max_connections=max_connections,
                decode_responses=True
            )
            
            # 创建客户端
            self.client = redis.Redis(
                connection_pool=self.pool,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            
            self.logger = logging.getLogger(__name__)
        
        def set(
            self,
            key: str,
            value: Any,
            expire: Optional[int] = None
        ) -> bool:
            """设置键值"""
            try:
                # 序列化值
                serialized_value = json.dumps(value, ensure_ascii=False)
                
                # 设置键值
                if expire:
                    return self.client.setex(key, expire, serialized_value)
                else:
                    return self.client.set(key, serialized_value)
            
            except Exception as e:
                self.logger.error(f"Redis set error: {e}")
                return False
        
        def get(self, key: str) -> Optional[Any]:
            """获取键值"""
            try:
                value = self.client.get(key)
                if value is None:
                    return None
                
                # 反序列化
                return json.loads(value)
            
            except Exception as e:
                self.logger.error(f"Redis get error: {e}")
                return None
        
        def delete(self, key: str) -> bool:
            """删除键"""
            try:
                return self.client.delete(key) > 0
            except Exception as e:
                self.logger.error(f"Redis delete error: {e}")
                return False
        
        def exists(self, key: str) -> bool:
            """检查键是否存在"""
            try:
                return self.client.exists(key) > 0
            except Exception as e:
                self.logger.error(f"Redis exists error: {e}")
                return False
        
        def hset(self, name: str, key: str, value: Any) -> bool:
            """设置 Hash 字段"""
            try:
                serialized_value = json.dumps(value, ensure_ascii=False)
                return self.client.hset(name, key, serialized_value) > 0
            except Exception as e:
                self.logger.error(f"Redis hset error: {e}")
                return False
        
        def hget(self, name: str, key: str) -> Optional[Any]:
            """获取 Hash 字段"""
            try:
                value = self.client.hget(name, key)
                if value is None:
                    return None
                return json.loads(value)
            except Exception as e:
                self.logger.error(f"Redis hget error: {e}")
                return None
        
        def hgetall(self, name: str) -> Dict[str, Any]:
            """获取所有 Hash 字段"""
            try:
                data = self.client.hgetall(name)
                return {k: json.loads(v) for k, v in data.items()}
            except Exception as e:
                self.logger.error(f"Redis hgetall error: {e}")
                return {}
        
        def close(self):
            """关闭连接"""
            self.pool.disconnect()

    # 使用示例
    redis_client = RedisClient(
        host="localhost",
        port=6379,
        db=0
    )

    # 设置值
    redis_client.set("user:123", {"name": "张三", "department": "工程部"}, expire=3600)

    # 获取值
    user_data = redis_client.get("user:123")
    print(user_data)

    # 使用 Hash
    redis_client.hset("session:456", "user_id", "123")
    redis_client.hset("session:456", "created_at", "2026-01-09")
    session_data = redis_client.hgetall("session:456")
    print(session_data)
    ```

##### 模块 2: 会话管理器 (Session Manager)
*   **核心概念**: 
    - Session ID 生成
    - 会话元数据管理
    - 会话过期策略
    - 多用户隔离
*   **实战任务**:
    - 实现 Session Manager 类
    - 实现会话创建、查询、更新、删除
    - 实现会话列表查询
    - 实现会话过期清理
*   **💻 代码示例**:
    ```python
    from typing import Optional, Dict, List
    from datetime import datetime
    import uuid

    class SessionManager:
        """会话管理器"""
        
        def __init__(self, redis_client: RedisClient):
            self.redis = redis_client
            self.session_prefix = "session:"
            self.session_expire = 7 * 24 * 3600  # 7 天
        
        def create_session(
            self,
            user_id: str,
            metadata: Optional[Dict] = None
        ) -> str:
            """创建新会话"""
            # 生成 Session ID
            session_id = str(uuid.uuid4())
            
            # 构建会话数据
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "message_count": 0,
                "metadata": metadata or {}
            }
            
            # 存储会话数据
            key = f"{self.session_prefix}{session_id}"
            self.redis.set(key, session_data, expire=self.session_expire)
            
            # 添加到用户的会话列表
            self._add_to_user_sessions(user_id, session_id)
            
            return session_id
        
        def get_session(self, session_id: str) -> Optional[Dict]:
            """获取会话信息"""
            key = f"{self.session_prefix}{session_id}"
            return self.redis.get(key)
        
        def update_session(
            self,
            session_id: str,
            updates: Dict
        ) -> bool:
            """更新会话信息"""
            key = f"{self.session_prefix}{session_id}"
            session_data = self.redis.get(key)
            
            if not session_data:
                return False
            
            # 更新数据
            session_data.update(updates)
            session_data["updated_at"] = datetime.now().isoformat()
            
            # 保存更新
            return self.redis.set(key, session_data, expire=self.session_expire)
        
        def delete_session(self, session_id: str) -> bool:
            """删除会话"""
            key = f"{self.session_prefix}{session_id}"
            session_data = self.redis.get(key)
            
            if not session_data:
                return False
            
            # 从用户的会话列表中移除
            user_id = session_data.get("user_id")
            self._remove_from_user_sessions(user_id, session_id)
            
            # 删除会话
            return self.redis.delete(key)
        
        def get_user_sessions(self, user_id: str) -> List[Dict]:
            """获取用户的所有会话"""
            key = f"user_sessions:{user_id}"
            session_ids = self.redis.get(key) or []
            
            sessions = []
            for session_id in session_ids:
                session_data = self.get_session(session_id)
                if session_data:
                    sessions.append(session_data)
            
            return sessions
        
        def _add_to_user_sessions(self, user_id: str, session_id: str):
            """添加到用户的会话列表"""
            key = f"user_sessions:{user_id}"
            session_ids = self.redis.get(key) or []
            
            if session_id not in session_ids:
                session_ids.insert(0, session_id)  # 添加到开头
            
            self.redis.set(key, session_ids, expire=self.session_expire)
        
        def _remove_from_user_sessions(self, user_id: str, session_id: str):
            """从用户的会话列表中移除"""
            key = f"user_sessions:{user_id}"
            session_ids = self.redis.get(key) or []
            
            if session_id in session_ids:
                session_ids.remove(session_id)
            
            self.redis.set(key, session_ids, expire=self.session_expire)

    # 使用示例
    session_manager = SessionManager(redis_client)

    # 创建会话
    session_id = session_manager.create_session(
        user_id="user123",
        metadata={"role": "new_employee"}
    )
    print(f"创建会话: {session_id}")

    # 获取会话
    session_data = session_manager.get_session(session_id)
    print(f"会话信息: {session_data}")

    # 更新会话
    session_manager.update_session(
        session_id,
        {"message_count": 5, "metadata": {"last_topic": "入职流程"}}
    )

    # 获取用户的所有会话
    user_sessions = session_manager.get_user_sessions("user123")
    print(f"用户会话: {len(user_sessions)} 个")
    ```

##### 模块 3: 上下文管理器 (Context Manager)
*   **核心概念**: 
    - 对话历史存储
    - 智能上下文压缩
    - Token 管理
    - 滑动窗口
*   **实战任务**:
    - 实现对话历史存储
    - 实现智能上下文压缩
    - 实现 Token 计数与管理
    - 实现滑动窗口记忆
*   **💻 代码示例**:
    ```python
    from typing import List, Dict, Optional
    from datetime import datetime

    class ContextManager:
        """上下文管理器"""
        
        def __init__(
            self,
            redis_client: RedisClient,
            max_history_length: int = 10,
            max_context_tokens: int = 4000
        ):
            self.redis = redis_client
            self.max_history_length = max_history_length
            self.max_context_tokens = max_context_tokens
            self.message_prefix = "messages:"
        
        def add_message(
            self,
            session_id: str,
            role: str,
            content: str,
            metadata: Optional[Dict] = None
        ) -> bool:
            """添加消息到历史"""
            key = f"{self.message_prefix}{session_id}"
            messages = self.redis.get(key) or []
            
            # 构建消息
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # 添加到历史
            messages.append(message)
            
            # 智能压缩
            compressed_messages = self._compress_context(messages)
            
            # 保存
            return self.redis.set(key, compressed_messages)
        
        def get_messages(self, session_id: str) -> List[Dict]:
            """获取消息历史"""
            key = f"{self.message_prefix}{session_id}"
            return self.redis.get(key) or []
        
        def get_context(
            self,
            session_id: str,
            max_tokens: Optional[int] = None
        ) -> List[Dict]:
            """获取压缩后的上下文"""
            messages = self.get_messages(session_id)
            max_tokens = max_tokens or self.max_context_tokens
            
            return self._compress_context(messages, max_tokens)
        
        def clear_history(self, session_id: str) -> bool:
            """清空历史"""
            key = f"{self.message_prefix}{session_id}"
            return self.redis.delete(key)
        
        def _compress_context(
            self,
            messages: List[Dict],
            max_tokens: Optional[int] = None
        ) -> List[Dict]:
            """压缩上下文"""
            max_tokens = max_tokens or self.max_context_tokens
            
            # 1. 限制消息数量
            if len(messages) > self.max_history_length:
                messages = messages[-self.max_history_length:]
            
            # 2. 限制 Token 数量
            current_tokens = self._count_tokens(messages)
            
            while current_tokens > max_tokens and len(messages) > 2:
                # 移除最早的消息（保留系统消息和最近的消息）
                messages = messages[1:]
                current_tokens = self._count_tokens(messages)
            
            return messages
        
        def _count_tokens(self, messages: List[Dict]) -> int:
            """估算 Token 数量"""
            # 简单估算：1 Token ≈ 4 字符（中文）
            total_chars = sum(
                len(msg.get('content', ''))
                for msg in messages
            )
            return total_chars // 4
        
        def get_summary(self, session_id: str) -> Dict:
            """获取对话摘要"""
            messages = self.get_messages(session_id)
            
            return {
                "total_messages": len(messages),
                "total_tokens": self._count_tokens(messages),
                "first_message": messages[0] if messages else None,
                "last_message": messages[-1] if messages else None,
                "user_messages": sum(1 for m in messages if m['role'] == 'user'),
                "assistant_messages": sum(1 for m in messages if m['role'] == 'assistant')
            }

    # 使用示例
    context_manager = ContextManager(
        redis_client,
        max_history_length=10,
        max_context_tokens=4000
    )

    # 添加消息
    context_manager.add_message(
        session_id="session123",
        role="user",
        content="你好，我是新员工"
    )

    context_manager.add_message(
        session_id="session123",
        role="assistant",
        content="欢迎加入公司！有什么可以帮助你的吗？"
    )

    # 获取上下文
    context = context_manager.get_context("session123")
    print(f"上下文消息数: {len(context)}")

    # 获取摘要
    summary = context_manager.get_summary("session123")
    print(f"对话摘要: {summary}")
    ```

---

#### Sprint 5: FastAPI 服务 ✅

**学习目标:**
- 掌握 FastAPI 框架
- 实现 OpenAI 兼容的 API
- 实现会话管理接口
- 实现统一错误处理与日志

**核心模块:**

##### 模块 1: FastAPI 应用初始化 (App Initialization)
*   **核心概念**: 
    - FastAPI 应用创建
    - CORS 配置
    - 中间件（Middleware）
    - 依赖注入（Dependency Injection）
*   **实战任务**:
    - 创建 FastAPI 应用
    - 配置 CORS
    - 添加日志中间件
    - 添加错误处理中间件
*   **💻 代码示例**:
    ```python
    from fastapi import FastAPI, Request, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import logging
    import time

    # 创建 FastAPI 应用
    app = FastAPI(
        title="Nexus Agent API",
        description="智能入职助手 API",
        version="0.5.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 日志中间件
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """记录所有请求"""
        start_time = time.time()
        
        # 记录请求
        logger.info(f"Request: {request.method} {request.url}")
        
        # 处理请求
        response = await call_next(request)
        
        # 记录响应
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Response: {response.status_code} ({process_time:.3f}s)")
        
        return response

    # 全局异常处理
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """全局异常处理器"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": str(exc),
                "path": str(request.url)
            }
        )

    # 健康检查端点
    @app.get("/v1/health")
    async def health_check():
        """健康检查"""
        return {
            "status": "ok",
            "version": "0.5.0",
            "timestamp": time.time()
        }
    ```

##### 模块 2: 聊天接口 (Chat API)
*   **核心概念**: 
    - OpenAI 兼容接口
    - 流式响应（Streaming）
    - 会话管理
    - 错误处理
*   **实战任务**:
    - 实现 `/v1/chat/completions` 接口
    - 支持流式和非流式响应
    - 集成会话管理
    - 实现错误处理
*   **💻 代码示例**:
    ```python
    from fastapi import APIRouter, HTTPException
    from pydantic import BaseModel, Field
    from typing import List, Optional, Literal
    from sse_starlette.sse import EventSourceResponse

    # 创建路由
    router = APIRouter(prefix="/v1", tags=["chat"])

    # 请求模型
    class ChatMessage(BaseModel):
        role: Literal["system", "user", "assistant"]
        content: str

    class ChatRequest(BaseModel):
        messages: List[ChatMessage]
        session_id: Optional[str] = None
        user: Optional[str] = None
        stream: bool = False
        temperature: Optional[float] = None

    class ChatResponse(BaseModel):
        id: str
        object: str = "chat.completion"
        created: int
        model: str
        choices: List[dict]
        usage: Optional[dict] = None

    @router.post("/chat/completions")
    async def chat_completions(request: ChatRequest):
        """聊天完成接口（OpenAI 兼容）"""
        try:
            # 获取或创建会话
            session_id = request.session_id or session_manager.create_session(
                user_id=request.user or "anonymous"
            )
            
            # 处理消息
            user_input = request.messages[-1].content
            
            # 调用 Agent
            response = agent.process_message(user_input)
            
            if not response.success:
                raise HTTPException(
                    status_code=500,
                    detail=response.error
                )
            
            # 保存消息到上下文
            context_manager.add_message(
                session_id,
                role="user",
                content=user_input
            )
            context_manager.add_message(
                session_id,
                role="assistant",
                content=response.content
            )
            
            # 更新会话
            session_manager.update_session(
                session_id,
                {"message_count": len(context_manager.get_messages(session_id))}
            )
            
            # 返回响应
            if request.stream:
                # 流式响应
                return EventSourceResponse(
                    _stream_response(response.content, session_id)
                )
            else:
                # 非流式响应
                return ChatResponse(
                    id=f"chatcmpl-{session_id}",
                    created=int(time.time()),
                    model="nexus-agent",
                    choices=[{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response.content
                        },
                        "finish_reason": "stop"
                    }]
                )
        
        except Exception as e:
            logger.error(f"Chat completion error: {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    async def _stream_response(content: str, session_id: str):
        """流式响应生成器"""
        words = content.split()
        for i, word in enumerate(words):
            chunk = {
                "id": f"chatcmpl-{session_id}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": "nexus-agent",
                "choices": [{
                    "index": 0,
                    "delta": {
                        "content": word + " "
                    },
                    "finish_reason": None
                }]
            }
            yield chunk
            await asyncio.sleep(0.01)  # 模拟打字机效果
        
        # 发送结束标记
        end_chunk = {
            "id": f"chatcmpl-{session_id}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "nexus-agent",
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
        yield end_chunk
    ```

##### 模块 3: 会话管理接口 (Session API)
*   **核心概念**: 
    - RESTful API 设计
    - 会话 CRUD 操作
    - 历史消息查询
    - 数据验证
*   **实战任务**:
    - 实现 POST `/v1/sessions/` - 创建会话
    - 实现 GET `/v1/sessions/{session_id}` - 获取会话
    - 实现 GET `/v1/sessions/{session_id}/history` - 获取历史
    - 实现 DELETE `/v1/sessions/{session_id}` - 删除会话
*   **💻 代码示例**:
    ```python
    from fastapi import APIRouter, HTTPException, Depends
    from pydantic import BaseModel

    # 创建路由
    session_router = APIRouter(prefix="/v1/sessions", tags=["sessions"])

    # 请求/响应模型
    class CreateSessionRequest(BaseModel):
        user_id: str
        metadata: Optional[dict] = None

    class SessionResponse(BaseModel):
        session_id: str
        user_id: str
        created_at: str
        updated_at: str
        message_count: int
        metadata: dict

    @session_router.post("/", response_model=SessionResponse)
    async def create_session(request: CreateSessionRequest):
        """创建新会话"""
        try:
            session_id = session_manager.create_session(
                user_id=request.user_id,
                metadata=request.metadata
            )
            
            session_data = session_manager.get_session(session_id)
            
            return SessionResponse(**session_data)
        
        except Exception as e:
            logger.error(f"Create session error: {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    @session_router.get("/{session_id}", response_model=SessionResponse)
    async def get_session(session_id: str):
        """获取会话信息"""
        session_data = session_manager.get_session(session_id)
        
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )
        
        return SessionResponse(**session_data)

    @session_router.get("/{session_id}/history")
    async def get_session_history(session_id: str):
        """获取会话历史消息"""
        messages = context_manager.get_messages(session_id)
        
        return {
            "session_id": session_id,
            "messages": messages,
            "total_messages": len(messages)
        }

    @session_router.delete("/{session_id}")
    async def delete_session(session_id: str):
        """删除会话"""
        success = session_manager.delete_session(session_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )
        
        return {"message": "Session deleted successfully"}

    @session_router.get("/user/{user_id}")
    async def get_user_sessions(user_id: str):
        """获取用户的所有会话"""
        sessions = session_manager.get_user_sessions(user_id)
        
        return {
            "user_id": user_id,
            "sessions": sessions,
            "total_sessions": len(sessions)
        }
    ```

---

#### Sprint 6: React 前端开发 ✅

**学习目标:**
- 掌握 React 18 + Hooks
- 实现模块化组件架构
- 集成 API 客户端
- 实现会话管理与持久化

**核心模块:**

##### 模块 1: 项目初始化 (Project Setup)
*   **核心概念**: 
    - Vite 构建工具
    - React 18
    - CSS Modules
    - 项目结构
*   **实战任务**:
    - 使用 Vite 创建 React 项目
    - 配置 CSS Modules
    - 设置项目结构
    - 配置 Axios 客户端
*   **💻 代码示例**:
    ```bash
    # 创建项目
    npm create vite@latest frontend -- --template react
    cd frontend

    # 安装依赖
    npm install axios react-markdown lucide-react

    # 项目结构
    frontend/
    ├── src/
    │   ├── api/
    │   │   └── client.js          # API 客户端
    │   ├── components/
    │   │   ├── ChatWindow.jsx      # 聊天窗口
    │   │   ├── ChatWindow.module.css
    │   │   ├── Sidebar.jsx         # 侧边栏
    │   │   └── Sidebar.module.css
    │   ├── App.jsx                # 根组件
    │   ├── App.css
    │   ├── main.jsx               # 入口
    │   └── index.css
    ├── public/
    ├── index.html
    ├── package.json
    └── vite.config.js
    ```

##### 模块 2: API 客户端 (API Client)
*   **核心概念**: 
    - Axios HTTP 客户端
    - 请求/响应拦截器
    - 错误处理
    - 自动重试
*   **实战任务**:
    - 封装 Axios 客户端
    - 实现请求拦截器
    - 实现响应拦截器
    - 实现错误处理
*   **💻 代码示例**:
    ```javascript
    // src/api/client.js
    import axios from 'axios';

    // 创建 Axios 实例
    const apiClient = axios.create({
        baseURL: 'http://localhost:8001',
        timeout: 30000,
        headers: {
            'Content-Type': 'application/json',
        },
    });

    // 请求拦截器
    apiClient.interceptors.request.use(
        (config) => {
            // 添加时间戳
            config.metadata = { startTime: new Date() };
            
            // 从 localStorage 获取 session_id
            const sessionId = localStorage.getItem('current_session_id');
            if (sessionId) {
                config.headers['X-Session-ID'] = sessionId;
            }
            
            console.log('Request:', config);
            return config;
        },
        (error) => {
            console.error('Request error:', error);
            return Promise.reject(error);
        }
    );

    // 响应拦截器
    apiClient.interceptors.response.use(
        (response) => {
            // 计算请求耗时
            const duration = new Date() - response.config.metadata.startTime;
            response.config.metadata.duration = duration;
            
            console.log('Response:', response);
            return response;
        },
        (error) => {
            console.error('Response error:', error);
            
            // 统一错误处理
            if (error.response) {
                // 服务器返回错误
                const { status, data } = error.response;
                
                if (status === 401) {
                    // 未授权
                    console.error('Unauthorized');
                } else if (status === 500) {
                    // 服务器错误
                    console.error('Server error:', data);
                }
            } else if (error.request) {
                // 请求发送但无响应
                console.error('No response:', error.request);
            } else {
                // 请求配置错误
                console.error('Request config error:', error.message);
            }
            
            return Promise.reject(error);
        }
    );

    // API 方法
    export const api = {
        // 健康检查
        health: () => apiClient.get('/v1/health'),
        
        // 聊天完成
        chat: (messages, sessionId, user) => {
            return apiClient.post('/v1/chat/completions', {
                messages,
                session_id: sessionId,
                user,
                stream: false
            });
        },
        
        // 创建会话
        createSession: (userId, metadata) => {
            return apiClient.post('/v1/sessions/', {
                user_id: userId,
                metadata
            });
        },
        
        // 获取会话
        getSession: (sessionId) => {
            return apiClient.get(`/v1/sessions/${sessionId}`);
        },
        
        // 获取会话历史
        getSessionHistory: (sessionId) => {
            return apiClient.get(`/v1/sessions/${sessionId}/history`);
        },
        
        // 删除会话
        deleteSession: (sessionId) => {
            return apiClient.delete(`/v1/sessions/${sessionId}`);
        },
        
        // 获取用户的所有会话
        getUserSessions: (userId) => {
            return apiClient.get(`/v1/sessions/user/${userId}`);
        }
    };

    export default apiClient;
    ```

##### 模块 3: 聊天窗口组件 (ChatWindow Component)
*   **核心概念**: 
    - React Hooks（useState, useEffect, useRef）
    - 事件处理
    - 乐观 UI 更新
    - Markdown 渲染
*   **实战任务**:
    - 实现聊天窗口 UI
    - 实现消息列表
    - 实现输入框
    - 实现发送消息功能
*   **💻 代码示例**:
    ```jsx
    // src/components/ChatWindow.jsx
    import React, { useState, useEffect, useRef } from 'react';
    import { Send, User, Bot } from 'lucide-react';
    import ReactMarkdown from 'react-markdown';
    import { api } from '../api/client';
    import styles from './ChatWindow.module.css';

    function ChatWindow({ currentSession, onNewMessage }) {
        const [messages, setMessages] = useState([]);
        const [input, setInput] = useState('');
        const [loading, setLoading] = useState(false);
        const messagesEndRef = useRef(null);

        // 自动滚动到底部
        const scrollToBottom = () => {
            messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
        };

        useEffect(() => {
            scrollToBottom();
        }, [messages]);

        // 加载会话历史
        useEffect(() => {
            if (currentSession) {
                loadSessionHistory(currentSession.session_id);
            }
        }, [currentSession]);

        const loadSessionHistory = async (sessionId) => {
            try {
                const response = await api.getSessionHistory(sessionId);
                setMessages(response.data.messages);
            } catch (error) {
                console.error('Failed to load session history:', error);
            }
        };

        const handleSendMessage = async () => {
            if (!input.trim() || loading) return;

            const userMessage = {
                role: 'user',
                content: input,
                timestamp: new Date().toISOString()
            };

            // 乐观更新
            setMessages(prev => [...prev, userMessage]);
            setInput('');
            setLoading(true);

            try {
                const response = await api.chat(
                    [...messages, userMessage],
                    currentSession?.session_id,
                    'user'
                );

                const assistantMessage = {
                    role: 'assistant',
                    content: response.data.choices[0].message.content,
                    timestamp: new Date().toISOString()
                };

                setMessages(prev => [...prev, assistantMessage]);
                
                // 通知父组件
                if (onNewMessage) {
                    onNewMessage(assistantMessage);
                }
            } catch (error) {
                console.error('Failed to send message:', error);
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: '抱歉，发送消息时出错了。请稍后重试。',
                    timestamp: new Date().toISOString()
                }]);
            } finally {
                setLoading(false);
            }
        };

        const handleKeyPress = (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        };

        return (
            <div className={styles.chatWindow}>
                <div className={styles.messagesContainer}>
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`${styles.message} ${styles[msg.role]}`}
                        >
                            <div className={styles.messageIcon}>
                                {msg.role === 'user' ? <User /> : <Bot />}
                            </div>
                            <div className={styles.messageContent}>
                                <ReactMarkdown>{msg.content}</ReactMarkdown>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className={`${styles.message} ${styles.assistant}`}>
                            <div className={styles.messageIcon}>
                                <Bot />
                            </div>
                            <div className={styles.messageContent}>
                                <div className={styles.typingIndicator}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <div className={styles.inputContainer}>
                    <textarea
                        className={styles.input}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="输入消息..."
                        disabled={loading}
                        rows={1}
                    />
                    <button
                        className={styles.sendButton}
                        onClick={handleSendMessage}
                        disabled={loading || !input.trim()}
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
        );
    }

    export default ChatWindow;
    ```

##### 模块 4: 侧边栏组件 (Sidebar Component)
*   **核心概念**: 
    - 会话列表管理
    - localStorage 持久化
    - 会话切换
    - 新建会话
*   **实战任务**:
    - 实现会话列表
    - 实现会话切换
    - 实现新建会话
    - 实现删除会话
*   **💻 代码示例**:
    ```jsx
    // src/components/Sidebar.jsx
    import React, { useState, useEffect } from 'react';
    import { Plus, Trash2, MessageSquare } from 'lucide-react';
    import { api } from '../api/client';
    import styles from './Sidebar.module.css';

    function Sidebar({ currentSession, onSessionSelect, onNewSession }) {
        const [sessions, setSessions] = useState([]);
        const [loading, setLoading] = useState(false);

        // 加载会话列表
        useEffect(() => {
            loadSessions();
        }, []);

        const loadSessions = async () => {
            try {
                const userId = localStorage.getItem('user_id') || 'demo_user';
                const response = await api.getUserSessions(userId);
                setSessions(response.data.sessions);
            } catch (error) {
                console.error('Failed to load sessions:', error);
            }
        };

        const handleCreateSession = async () => {
            setLoading(true);
            try {
                const userId = localStorage.getItem('user_id') || 'demo_user';
                const response = await api.createSession(userId, {
                    role: 'new_employee'
                });
                
                // 保存当前会话 ID
                localStorage.setItem('current_session_id', response.data.session_id);
                
                // 刷新会话列表
                await loadSessions();
                
                // 通知父组件
                if (onNewSession) {
                    onNewSession(response.data);
                }
            } catch (error) {
                console.error('Failed to create session:', error);
            } finally {
                setLoading(false);
            }
        };

        const handleDeleteSession = async (sessionId, event) => {
            event.stopPropagation();
            
            if (!confirm('确定要删除这个会话吗？')) return;

            try {
                await api.deleteSession(sessionId);
                
                // 刷新会话列表
                await loadSessions();
                
                // 如果删除的是当前会话，清空当前会话
                if (currentSession?.session_id === sessionId) {
                    localStorage.removeItem('current_session_id');
                    if (onSessionSelect) {
                        onSessionSelect(null);
                    }
                }
            } catch (error) {
                console.error('Failed to delete session:', error);
            }
        };

        const formatTime = (timestamp) => {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now - date;
            
            if (diff < 60000) return '刚刚';
            if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`;
            if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`;
            return date.toLocaleDateString();
        };

        return (
            <div className={styles.sidebar}>
                <div className={styles.sidebarHeader}>
                    <h2>会话</h2>
                    <button
                        className={styles.newSessionButton}
                        onClick={handleCreateSession}
                        disabled={loading}
                    >
                        <Plus size={20} />
                        新建会话
                    </button>
                </div>

                <div className={styles.sessionList}>
                    {sessions.map((session) => (
                        <div
                            key={session.session_id}
                            className={`${styles.sessionItem} ${
                                currentSession?.session_id === session.session_id
                                    ? styles.active
                                    : ''
                            }`}
                            onClick={() => onSessionSelect?.(session)}
                        >
                            <div className={styles.sessionInfo}>
                                <MessageSquare size={16} />
                                <div className={styles.sessionDetails}>
                                    <div className={styles.sessionTitle}>
                                        会话 {session.session_id.slice(0, 8)}
                                    </div>
                                    <div className={styles.sessionMeta}>
                                        <span>{session.message_count} 条消息</span>
                                        <span>{formatTime(session.updated_at)}</span>
                                    </div>
                                </div>
                            </div>
                            <button
                                className={styles.deleteButton}
                                onClick={(e) => handleDeleteSession(session.session_id, e)}
                            >
                                <Trash2 size={16} />
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    export default Sidebar;
    ```

---

## 📚 学习方法论 (Methodology)

### 1. Code-First (代码优先)
- **原则**: 不讲空洞理论，每个模块结束时必须产出可运行的代码
- **实践**: 
    - 每个模块都有完整的代码示例
    - 提供可直接运行的演示脚本
    - 代码包含详细的中文注释
    - 遵循 LangChain 1.0 最佳实践

### 2. Fail Fast (快速试错)
- **原则**: 故意写出有 Bug 的代码，然后在调试中学习
- **实践**:
    - 演示常见错误（如 Context 溢出）
    - 提供错误诊断和修复方案
    - 包含完整的测试用例
    - 提供调试技巧和工具

### 3. Enterprise Reality (面向企业)
- **原则**: 关注真实痛点——脏数据清洗、API 超时重试、Token 成本控制
- **实践**:
    - 实现数据预处理工具
    - 实现错误处理和重试机制
    - 实现 Token 管理和成本优化
    - 实现日志追踪和监控

### 4. Test-Driven (测试驱动)
- **原则**: 编写全面的测试用例，确保代码质量
- **实践**:
    - 单元测试（26 个工具测试用例）
    - 集成测试（19 个工具调用测试用例）
    - 测试覆盖率 > 90%
    - 使用 pytest 和 Mock

### 5. Documentation-First (文档优先)
- **原则**: 详细的文档和注释，方便学习和维护
- **实践**:
    - 每个模块都有详细的文档
    - 代码包含详细的中文注释
    - 提供使用示例和最佳实践
    - 维护 PROJECT_GUIDE 和 README

---

## 🎓 学习路径建议

### 第一阶段：环境搭建与基础理解（1-2 周）
1. **环境准备**
   - 安装 Python 3.10+
   - 安装 UV 包管理器
   - 安装 Redis
   - 配置环境变量

2. **项目理解**
   - 阅读 [`README.md`](../README.md)
   - 阅读 [`PROJECT_GUIDE.md`](../PROJECT_GUIDE.md)
   - 阅读 [`Quick-Start-Guide.md`](./Quick-Start-Guide.md)

3. **运行项目**
   - 使用 `./scripts/start_all.sh` 启动所有服务
   - 访问 http://localhost:5173 测试前端
   - 访问 http://localhost:8001/docs 查看 API 文档

### 第二阶段：核心模块学习（2-3 周）
1. **Sprint 1: 基础对话系统**
   - 学习 [`nexus_agent/agent/agent.py`](../nexus_agent/agent/agent.py)
   - 学习 [`nexus_agent/agent/middleware.py`](../nexus_agent/agent/middleware.py)
   - 运行 [`demos/demo_script.py`](../demos/demo_script.py)

2. **Sprint 2: RAG 知识检索**
   - 学习 [`nexus_agent/rag/`](../nexus_agent/rag/) 模块
   - 运行 [`demos/demo_rag.py`](../demos/demo_rag.py)
   - 运行 [`demos/demo_document_processing.py`](../demos/demo_document_processing.py)

3. **Sprint 3: 工具调用系统**
   - 学习 [`nexus_agent/agent/api_tools.py`](../nexus_agent/agent/api_tools.py)
   - 运行 [`demos/demo_tool_calling.py`](../demos/demo_tool_calling.py)
   - 运行测试套件

### 第三阶段：进阶功能学习（2-3 周）
1. **Sprint 4: Redis 记忆管理**
   - 学习 [`nexus_agent/storage/`](../nexus_agent/storage/) 模块
   - 运行 [`demos/demo_memory_management.py`](../demos/demo_memory_management.py)

2. **Sprint 5: FastAPI 服务**
   - 学习 [`nexus_agent/api/`](../nexus_agent/api/) 模块
   - 运行 [`scripts/run_server.py`](../scripts/run_server.py)
   - 测试 API 接口

3. **Sprint 6: React 前端开发**
   - 学习 [`frontend/`](../frontend/) 模块
   - 启动前端开发服务器
   - 测试前后端联调

### 第四阶段：实践与扩展（持续）
1. **添加新功能**
   - 添加新的 LLM 提供商
   - 实现新的工具
   - 添加新的检索策略
   - 实现新的中间件

2. **优化现有功能**
   - 优化检索准确性
   - 减少 Token 消耗
   - 提高响应速度
   - 改进用户体验

3. **部署与运维**
   - Docker 容器化
   - CI/CD 流水线
   - 监控与告警
   - 性能优化

---

## 📖 相关文档索引

### 项目文档
- [`README.md`](../README.md) - 项目概述和快速开始
- [`PROJECT_GUIDE.md`](../PROJECT_GUIDE.md) - 详细的项目学习指南
- [`Quick-Start-Guide.md`](./Quick-Start-Guide.md) - 快速开始指南

### Sprint 计划文档
- [`plans/sprint1-prototype-plan.md`](../plans/sprint1-prototype-plan.md) - Sprint 1 计划
- [`plans/sprint2-rag-basics-plan.md`](../plans/sprint2-rag-basics-plan.md) - Sprint 2 计划
- [`plans/sprint3-tool-calling-plan.md`](../plans/sprint3-tool-calling-plan.md) - Sprint 3 计划
- [`plans/sprint4-memory-management-plan.md`](../plans/sprint4-memory-management-plan.md) - Sprint 4 计划
- [`plans/sprint5-fastapi-plan.md`](../plans/sprint5-fastapi-plan.md) - Sprint 5 计划
- [`plans/sprint6-frontend-development.md`](../plans/sprint6-frontend-development.md) - Sprint 6 计划

### 技术文档
- [`plans/langchain-1.0-syntax-guide.md`](../plans/langchain-1.0-syntax-guide.md) - LangChain 1.0 语法指南
- [`document/CORS-Issue-Resolution.md`](./CORS-Issue-Resolution.md) - CORS 问题解决方案
- [`document/CORS-Fix-Summary.md`](./CORS-Fix-Summary.md) - CORS 修复总结

### 测试文档
- [`test/Sprint4-Test-Report.md`](../test/Sprint4-Test-Report.md) - Sprint 4 测试报告

---

## 🚀 快速开始

### 一键启动（推荐）
```bash
# 启动所有服务（Redis + 后端 + 前端）
./scripts/start_all.sh
```

### 手动启动
```bash
# 终端 1: 启动 Redis
redis-server --daemonize yes

# 终端 2: 启动后端
python scripts/run_server.py

# 终端 3: 启动前端
cd frontend
npm run dev
```

### 访问应用
- **前端应用**: http://localhost:5173
- **后端 API**: http://localhost:8001
- **API 文档**: http://localhost:8001/docs

---

## 🎯 下一步计划

### Sprint 7: 高级功能与优化（规划中）
- 多模态支持（图像、音频）
- 知识图谱集成
- 个性化推荐
- 前端功能增强（聊天历史、搜索、导出）

### Sprint 8: 生产部署（规划中）
- Docker 容器化
- Kubernetes 部署
- CI/CD 流水线
- 监控与告警

---

## 📞 联系方式

如有问题或建议，请：
- 提交 Issue
- 查看 [项目文档](../document/)
- 阅读 [PROJECT_GUIDE.md](../PROJECT_GUIDE.md)

---

**Nexus Agent** - 帮助新员工快速适应工作环境，提高工作效率 🚀

**最后更新**: 2026-01-09
