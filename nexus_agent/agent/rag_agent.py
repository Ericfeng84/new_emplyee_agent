"""
RAG Agent module for Nexus Agent.

Provides RAG-enabled agent using LangChain 1.0 patterns with retrieval tool.
Combines conversational abilities with knowledge retrieval from the vector store.
"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class NexusRAGAgent:
    """
    RAG-enabled Nexus agent using LangChain 1.0 patterns.
    
    Combines conversational abilities with knowledge retrieval from
    the company knowledge base using a retrieval tool.
    """
    
    def __init__(
        self,
        model,
        vector_store,
        system_prompt: Optional[str] = None,
        retrieval_k: int = 3,
        verbose: bool = False,
    ):
        """
        Initialize the RAG agent.
        
        Args:
            model: LangChain chat model (e.g., ChatOpenAI)
            vector_store: VectorStore instance (NexusVectorStore)
            system_prompt: Custom system prompt (uses default if None)
            retrieval_k: Number of documents to retrieve
            verbose: Whether to print detailed logs
        """
        self.model = model
        self.vector_store = vector_store
        self.retrieval_k = retrieval_k
        self.verbose = verbose
        
        # Create retrieval tool
        self.retrieve_context_tool = self._create_retrieval_tool()
        
        # Define system prompt
        if system_prompt is None:
            system_prompt = self._get_default_system_prompt()
        
        # Create RAG agent using LangChain 1.0 syntax
        # Note: In LangChain 1.0, create_agent returns an agent directly
        # that can be invoked with messages, not an AgentExecutor
        self.agent = create_agent(
            model,
            tools=[self.retrieve_context_tool],
            system_prompt=system_prompt
        )
        
        logger.info("RAG agent initialized successfully")
    
    def _create_retrieval_tool(self):
        """
        Create a retrieval tool for the agent.
        
        Returns both content and artifacts (raw documents) for better
        transparency and debugging.
        """
        @tool
        def retrieve_context(query: str) -> str:
            """
            从公司知识库中检索相关信息，以帮助回答用户关于公司政策、流程和IT支持的问题。
            
            Args:
                query: 搜索查询以查找相关信息
                
            Returns:
                检索到的上下文信息，包含来源和内容
            """
            if self.verbose:
                logger.info(f"Retrieving context for: {query}")
            
            # Perform similarity search
            retrieved_docs = self.vector_store.similarity_search(
                query,
                k=self.retrieval_k
            )
            
            if not retrieved_docs:
                if self.verbose:
                    logger.warning("No documents retrieved")
                return "未找到相关信息。"
            
            # Serialize documents for the model
            context_parts = []
            for i, doc in enumerate(retrieved_docs, 1):
                source = doc.metadata.get('source', '未知来源')
                file_name = doc.metadata.get('file_name', '未知文件')
                content = doc.page_content
                
                context_parts.append(
                    f"【来源 {i}】\n"
                    f"文件: {file_name}\n"
                    f"路径: {source}\n"
                    f"内容: {content}"
                )
            
            serialized = "\n\n".join(context_parts)
            
            if self.verbose:
                logger.info(f"Retrieved {len(retrieved_docs)} documents")
            
            return serialized
        
        return retrieve_context
    
    def _get_default_system_prompt(self) -> str:
        """
        Get the default system prompt for the RAG agent.
        
        Returns:
            Default system prompt string
        """
        return """你是一个名为 Nexus 的智能助手，专门为公司新员工提供入职支持和工作协助。

## 你的角色定位
- **身份**: 公司内部 AI 助手，专注于新员工入职体验
- **语气**: 专业、热情、耐心、友好
- **边界**: 只回答与工作相关的问题，不涉及个人隐私或敏感信息

## 你的核心能力
1. **知识检索**: 使用检索工具从公司知识库中查找相关信息
2. **工作协助**: 基于检索到的信息提供准确的答案
3. **资源指引**: 引导员工找到正确的信息和联系人

## 使用知识库的原则
- 在回答问题前，先使用检索工具查找相关信息
- 基于检索到的内容提供准确、具体的答案
- 如果检索到的信息不足以回答问题，诚实说明并建议联系相关部门
- 引用信息来源，让用户知道答案来自哪里
- 不要编造或猜测信息

## 交互原则
- 始终保持专业和礼貌的语气
- 如果不确定答案，诚实说明并建议联系相关部门
- 不处理涉及薪资、个人隐私等敏感信息的请求
- 鼓励新员工提出问题，营造支持性的氛围
- 使用清晰、简洁的语言回答问题

## 安全边界
- 拒绝回答非工作相关问题
- 不存储或处理个人敏感信息
- 遇到不当请求时，礼貌地引导回工作话题
- 不提供法律或医疗建议

请记住：你的目标是帮助新员工快速适应工作环境，提高工作效率。
"""
    
    def query(
        self,
        user_input: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        stream: bool = False,
    ) -> AIMessage:
        """
        Process a user query with RAG capabilities.
        
        Args:
            user_input: User's question or request
            chat_history: Optional conversation history
            stream: Whether to stream the response
            
        Returns:
            Agent response as AIMessage
        """
        if self.verbose:
            logger.info(f"Processing query: {user_input[:100]}...")
        
        # Prepare messages
        messages = []
        
        if chat_history:
            # Convert chat history to message format
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current user message
        messages.append(HumanMessage(content=user_input))
        
        if stream:
            # Stream the response
            return self.agent.stream({"messages": messages})
        else:
            # Get complete response
            response = self.agent.invoke({"messages": messages})
            
            # LangChain 1.0 的 create_agent 返回格式为 {"messages": [...]}
            # 最后一条消息是 AI 的回复
            last_message = response["messages"][-1]
            
            if self.verbose:
                logger.info(f"Response generated: {len(last_message.content)} characters")
            
            return AIMessage(content=last_message.content)
    
    def stream_query(
        self,
        user_input: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ):
        """
        Stream a user query with RAG capabilities.
        
        Args:
            user_input: User's question or request
            chat_history: Optional conversation history
            
        Yields:
            Streaming response chunks
        """
        if self.verbose:
            logger.info(f"Streaming query: {user_input[:100]}...")
        
        # Prepare messages
        messages = []
        
        if chat_history:
            # Convert chat history to message format
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current user message
        messages.append(HumanMessage(content=user_input))
        
        # Stream the response
        for chunk in self.agent.stream({"messages": messages}):
            yield chunk
    
    def get_retrieval_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG agent's retrieval configuration.
        
        Returns:
            Dictionary with retrieval statistics
        """
        collection_stats = self.vector_store.get_collection_stats()
        
        return {
            'retrieval_k': self.retrieval_k,
            'collection_name': collection_stats.get('name', 'unknown'),
            'collection_count': collection_stats.get('count', 0),
            'verbose': self.verbose,
        }


class NexusRAGAgentWithMemory(NexusRAGAgent):
    """
    RAG agent with conversation memory support.
    
    Maintains conversation history for multi-turn interactions.
    """
    
    def __init__(
        self,
        model,
        vector_store,
        system_prompt: Optional[str] = None,
        retrieval_k: int = 3,
        max_history_length: int = 10,
        verbose: bool = False,
    ):
        """
        Initialize the RAG agent with memory.
        
        Args:
            model: LangChain chat model
            vector_store: VectorStore instance
            system_prompt: Custom system prompt
            retrieval_k: Number of documents to retrieve
            max_history_length: Maximum number of messages to keep in history
            verbose: Whether to print detailed logs
        """
        super().__init__(
            model=model,
            vector_store=vector_store,
            system_prompt=system_prompt,
            retrieval_k=retrieval_k,
            verbose=verbose,
        )
        
        self.max_history_length = max_history_length
        self.chat_history: List[Dict[str, str]] = []
        
        logger.info(f"RAG agent with memory initialized (max_history={max_history_length})")
    
    def query(
        self,
        user_input: str,
        stream: bool = False,
    ) -> AIMessage:
        """
        Process a user query with conversation memory.
        
        Args:
            user_input: User's question or request
            stream: Whether to stream the response
            
        Returns:
            Agent response as AIMessage
        """
        # Add user message to history
        self.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response using parent method with history
        response = super().query(
            user_input=user_input,
            chat_history=self.chat_history,
            stream=stream,
        )
        
        # Add assistant response to history
        self.chat_history.append({
            "role": "assistant",
            "content": response.content
        })
        
        # Trim history if needed
        if len(self.chat_history) > self.max_history_length:
            # Keep most recent messages
            self.chat_history = self.chat_history[-self.max_history_length:]
        
        return response
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.chat_history.clear()
        logger.info("Conversation history cleared")
    
    def get_history_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the conversation history.
        
        Returns:
            Dictionary with history summary
        """
        return {
            'total_messages': len(self.chat_history),
            'user_messages': sum(1 for msg in self.chat_history if msg["role"] == "user"),
            'assistant_messages': sum(1 for msg in self.chat_history if msg["role"] == "assistant"),
            'max_history_length': self.max_history_length,
        }
