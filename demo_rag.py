"""
RAG Demo Script for Nexus Agent.

Demonstrates the complete RAG pipeline including document indexing,
retrieval, and agent-based question answering.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 加载 .env 文件中的环境变量
load_dotenv()
from nexus_agent.rag.indexing import NexusIndexingPipeline
from nexus_agent.agent.rag_agent import NexusRAGAgentWithMemory
from nexus_agent.rag.retrieval import create_retriever


def run_rag_demo():
    """
    Run complete RAG demonstration.
    
    This demo shows:
    1. Document indexing
    2. Knowledge retrieval
    3. Agent-based question answering
    4. Multi-turn conversation with memory
    """
    print("=" * 70)
    print("Nexus Agent RAG Demo")
    print("=" * 70)
    print()
    
    # Check for API key
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Warning: DEEPSEEK_API_KEY or OPENAI_API_KEY not found in environment variables")
        print("   Please set DEEPSEEK_API_KEY to use the RAG agent with DeepSeek")
        print("   Demo will continue with indexing and retrieval only")
        print()
    
    # Step 1: Index documents
    print("Step 1: Indexing documents...")
    print("-" * 70)
    
    pipeline = NexusIndexingPipeline(
        data_dir="nexus_agent/data/documents",
        chunk_size=1000,
        chunk_overlap=200,
        embedding_model="BAAI/bge-small-zh-v1.5",
        embedding_device="cpu",
        persist_directory=None,  # In-memory for demo
    )
    
    stats = pipeline.index_documents(verbose=True)
    print()
    
    # Step 2: Test retrieval
    print("Step 2: Testing knowledge retrieval...")
    print("-" * 70)
    print()
    
    test_queries = [
        "公司的远程办公政策是什么？",
        "我如何配置VPN？",
        "我每年有多少天年假？",
        "如果忘记密码该怎么办？",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        results = pipeline.test_retrieval(query, k=2, verbose=False)
        print(f"Found {len(results)} relevant document(s)")
        print()
    
    # Step 3: Create RAG agent (if API key is available)
    if api_key:
        print("Step 3: Creating RAG agent...")
        print("-" * 70)
        
        # 使用 DeepSeek 模型作为默认配置
        # DeepSeek API 兼容 OpenAI 接口，通过配置 base_url 和 model 即可使用
        model = ChatOpenAI(
            model="deepseek-chat",  # DeepSeek 聊天模型
            temperature=0.7,
            openai_api_key=api_key,
            base_url="https://api.deepseek.com"  # DeepSeek API 端点
        )
        
        agent = NexusRAGAgentWithMemory(
            model=model,
            vector_store=pipeline.vector_store,
            retrieval_k=3,
            max_history_length=10,
            verbose=False
        )
        
        print("✅ RAG agent created with conversation memory")
        print()
        
        # Step 4: Test agent queries
        print("Step 4: Testing agent responses...")
        print("-" * 70)
        print()
        
        agent_test_queries = [
            "公司的远程办公政策是什么？",
            "我如何配置VPN？",
            "我每年有多少天年假？",
            "如果忘记密码该怎么办？",
        ]
        
        for i, query in enumerate(agent_test_queries, 1):
            print(f"Query {i}: {query}")
            print("-" * 70)
            
            response = agent.query(query)
            print(f"Nexus: {response.content}")
            print()
            print("=" * 70)
            print()
        
        # Step 5: Test multi-turn conversation
        print("Step 5: Testing multi-turn conversation...")
        print("-" * 70)
        print()
        
        print("User: 我如何申请休假？")
        response1 = agent.query("我如何申请休假？")
        print(f"Nexus: {response1.content}")
        print()
        
        print("User: 那病假呢？")
        response2 = agent.query("那病假呢？")
        print(f"Nexus: {response2.content}")
        print()
        
        # Show conversation history
        history_summary = agent.get_history_summary()
        print(f"Conversation history: {history_summary['total_messages']} messages")
        print(f"  - User messages: {history_summary['user_messages']}")
        print(f"  - Assistant messages: {history_summary['assistant_messages']}")
        print()
    
    else:
        print("Step 3-5: Skipped (requires OPENAI_API_KEY)")
        print("-" * 70)
        print()
        print("To test the RAG agent, set your DeepSeek API key:")
        print("  export DEEPSEEK_API_KEY='your-api-key-here'")
        print()
        print("Or set OpenAI API key as fallback:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    # Step 6: Demonstrate different retrieval strategies
    print("Step 6: Demonstrating retrieval strategies...")
    print("-" * 70)
    print()
    
    query = "远程办公政策"
    
    # Similarity search
    print("Strategy 1: Similarity Search")
    print(f"Query: {query}")
    sim_results = pipeline.vector_store.similarity_search(query, k=2)
    print(f"Found {len(sim_results)} results")
    for i, doc in enumerate(sim_results, 1):
        print(f"  {i}. {doc.page_content[:100]}...")
    print()
    
    # MMR search
    print("Strategy 2: Maximum Marginal Relevance (MMR)")
    print(f"Query: {query}")
    mmr_results = pipeline.vector_store.max_marginal_relevance_search(
        query,
        k=2,
        fetch_k=5,
        lambda_mult=0.5
    )
    print(f"Found {len(mmr_results)} results")
    for i, doc in enumerate(mmr_results, 1):
        print(f"  {i}. {doc.page_content[:100]}...")
    print()
    
    # Search with scores
    print("Strategy 3: Similarity Search with Scores")
    print(f"Query: {query}")
    score_results = pipeline.vector_store.similarity_search_with_score(query, k=2)
    print(f"Found {len(score_results)} results")
    for i, (doc, score) in enumerate(score_results, 1):
        print(f"  {i}. Score: {score:.4f}")
        print(f"     {doc.page_content[:100]}...")
    print()
    
    # Final summary
    print("=" * 70)
    print("Demo Summary")
    print("=" * 70)
    print(f"✅ Documents indexed: {stats['indexed_documents']}")
    print(f"✅ Average chunk size: {stats['average_chunk_size']:.0f} characters")
    print(f"✅ Total processing time: {stats['elapsed_time']:.2f} seconds")
    print(f"✅ Processing rate: {stats['total_chunks'] / stats['elapsed_time']:.1f} chunks/second")
    print()
    print("Demo completed successfully!")
    print()


def run_interactive_demo():
    """
    Run interactive demo with user input.
    
    Allows users to ask questions and see RAG agent responses.
    """
    print("=" * 70)
    print("Nexus Agent Interactive RAG Demo")
    print("=" * 70)
    print()
    
    # Check for API key
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Error: DEEPSEEK_API_KEY or OPENAI_API_KEY not found")
        print("   Please set DEEPSEEK_API_KEY to use interactive mode with DeepSeek")
        print()
        return
    
    # Index documents
    print("Indexing documents...")
    pipeline = NexusIndexingPipeline(
        data_dir="nexus_agent/data/documents",
        chunk_size=1000,
        chunk_overlap=200,
        embedding_model="BAAI/bge-small-zh-v1.5",
        persist_directory=None,
    )
    
    pipeline.index_documents(verbose=False)
    print("✅ Documents indexed")
    print()
    
    # Create agent
    # 使用 DeepSeek 模型作为默认配置
    # DeepSeek API 兼容 OpenAI 接口，通过配置 base_url 和 model 即可使用
    model = ChatOpenAI(
        model="deepseek-chat",  # DeepSeek 聊天模型
        temperature=0.7,
        openai_api_key=api_key,
        base_url="https://api.deepseek.com"  # DeepSeek API 端点
    )
    
    agent = NexusRAGAgentWithMemory(
        model=model,
        vector_store=pipeline.vector_store,
        retrieval_k=3,
        verbose=False
    )
    
    print("Interactive mode started!")
    print("Type your questions about company policies and IT support.")
    print("Type 'quit' or 'exit' to end the session.")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print()
                print("Goodbye!")
                break
            
            # Get agent response
            response = agent.query(user_input)
            print(f"Nexus: {response.content}")
            print()
            
        except KeyboardInterrupt:
            print()
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_demo()
    else:
        run_rag_demo()
