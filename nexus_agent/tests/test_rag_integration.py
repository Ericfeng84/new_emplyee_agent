"""
Integration tests for RAG system.

Tests end-to-end RAG flow including indexing, retrieval,
and agent responses.
"""

import pytest
from langchain_openai import ChatOpenAI
from nexus_agent.rag.indexing import NexusIndexingPipeline
from nexus_agent.agent.rag_agent import NexusRAGAgent, NexusRAGAgentWithMemory
from nexus_agent.rag.retrieval import create_retriever

# Skip agent tests if OpenAI API key is not available
import os
HAS_OPENAI_KEY = bool(os.getenv("OPENAI_API_KEY"))


class TestRAGIntegration:
    """Integration tests for complete RAG system."""
    
    @pytest.fixture
    def indexing_pipeline(self, tmp_path):
        """Setup indexing pipeline for testing."""
        # Create test documents
        (tmp_path / "employee_handbook.md").write_text("""
# 员工手册

## 远程办公政策
公司支持弹性工作制，员工可以在8:00-20:00之间灵活安排工作时间。
每周最多可远程办公2天，需提前一天申请。

## 休假政策
- 年假：入职第一年5天，第二至五年10天，五年以上15天
- 病假：每年15天带薪病假
- 事假：每年5天带薪事假
""")
        
        (tmp_path / "it_support.md").write_text("""
# IT支持文档

## VPN配置
1. 访问IT支持门户下载VPN客户端
2. 输入服务器地址：vpn.company.com
3. 使用公司邮箱和密码登录
4. 首次连接需安装证书

## 密码重置
1. 访问 https://account.company.com
2. 点击"忘记密码"
3. 输入公司邮箱
4. 按邮件提示重置密码
""")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,  # In-memory for testing
            embedding_model="BAAI/bge-small-zh-v1.5",
            chunk_size=500,
            chunk_overlap=100
        )
        
        pipeline.index_documents(verbose=False)
        return pipeline
    
    @pytest.fixture
    def rag_agent(self, indexing_pipeline):
        """Setup RAG agent for testing."""
        # Create a mock model for testing
        # Note: In real usage, you would use a real API key
        model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key="test-key"  # This will fail without real key
        )
        
        agent = NexusRAGAgent(
            model=model,
            vector_store=indexing_pipeline.vector_store,
            retrieval_k=3,
            verbose=False
        )
        
        return agent
    
    def test_indexing_pipeline_creates_embeddings(self, indexing_pipeline):
        """Test that indexing pipeline creates embeddings."""
        stats = indexing_pipeline.get_pipeline_status()
        
        assert stats['collection_count'] > 0
        assert stats['embedding_model'] == "BAAI/bge-small-zh-v1.5"
    
    def test_retrieval_finds_relevant_documents(self, indexing_pipeline):
        """Test that retrieval finds relevant Chinese documents."""
        results = indexing_pipeline.test_retrieval(
            "远程办公政策是什么？",
            k=2,
            verbose=False
        )
        
        assert len(results) > 0
        # Check that results contain relevant content
        content = " ".join([doc.page_content for doc in results])
        assert any(keyword in content for keyword in ["远程", "办公", "弹性"])
    
    def test_retrieval_with_vpn_query(self, indexing_pipeline):
        """Test retrieval with VPN-related query."""
        results = indexing_pipeline.vector_store.similarity_search(
            "如何配置VPN",
            k=2
        )
        
        assert len(results) == 2
        content = " ".join([doc.page_content for doc in results])
        assert "VPN" in content or "vpn" in content
    
    def test_retrieval_with_password_query(self, indexing_pipeline):
        """Test retrieval with password-related query."""
        results = indexing_pipeline.vector_store.similarity_search(
            "忘记密码怎么办",
            k=2
        )
        
        assert len(results) == 2
        content = " ".join([doc.page_content for doc in results])
        assert any(keyword in content for keyword in ["密码", "重置"])
    
    def test_retriever_creation(self, indexing_pipeline):
        """Test creating retriever from vector store."""
        retriever = create_retriever(
            indexing_pipeline.vector_store,
            search_type="similarity",
            k=3
        )
        
        results = retriever.invoke("远程办公")
        
        assert len(results) > 0
        assert len(results) <= 3
    
    def test_mmr_retrieval(self, indexing_pipeline):
        """Test maximum marginal relevance retrieval."""
        retriever = create_retriever(
            indexing_pipeline.vector_store,
            search_type="mmr",
            k=2,
            fetch_k=5,
            lambda_mult=0.5
        )
        
        results = retriever.invoke("休假政策")
        
        assert len(results) == 2
    
    def test_thresholded_retrieval(self, indexing_pipeline):
        """Test retrieval with score threshold."""
        retriever = create_retriever(
            indexing_pipeline.vector_store,
            search_type="similarity_score_threshold",
            k=5,
            score_threshold=0.5
        )
        
        results = retriever.invoke("远程办公")
        
        # Results should be limited by threshold
        assert len(results) <= 5
    
    @pytest.mark.skip(reason="Requires real API key")
    def test_rag_agent_query(self, rag_agent):
        """Test that agent can query and respond."""
        # This test requires a real API key, so we skip it by default
        response = rag_agent.query("公司的远程办公政策是什么？")
        
        assert response is not None
        assert len(response.content) > 0
    
    @pytest.mark.skip(reason="Requires real API key")
    def test_rag_agent_with_multiple_queries(self, rag_agent):
        """Test agent with multiple queries."""
        queries = [
            "公司的远程办公政策是什么？",
            "我如何配置VPN？",
            "我每年有多少天年假？"
        ]
        
        for query in queries:
            response = rag_agent.query(query)
            assert response is not None
            assert len(response.content) > 0
    
    @pytest.mark.skip(reason="Requires real API key")
    def test_rag_agent_with_memory(self, indexing_pipeline):
        """Test RAG agent with conversation memory."""
        model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key="test-key"
        )
        
        agent = NexusRAGAgentWithMemory(
            model=model,
            vector_store=indexing_pipeline.vector_store,
            retrieval_k=3,
            max_history_length=5,
            verbose=False
        )
        
        # First query
        response1 = agent.query("我如何申请休假？")
        assert response1 is not None
        
        # Check history
        history_summary = agent.get_history_summary()
        assert history_summary['total_messages'] == 2  # User + Assistant
        assert history_summary['user_messages'] == 1
        assert history_summary['assistant_messages'] == 1
        
        # Follow-up query
        response2 = agent.query("那病假呢？")
        assert response2 is not None
        
        # Check updated history
        history_summary = agent.get_history_summary()
        assert history_summary['total_messages'] == 4
    
    @pytest.mark.skip(reason="Requires real API key")
    def test_rag_agent_clear_history(self, indexing_pipeline):
        """Test clearing conversation history."""
        model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key="test-key"
        )
        
        agent = NexusRAGAgentWithMemory(
            model=model,
            vector_store=indexing_pipeline.vector_store,
            retrieval_k=3,
            verbose=False
        )
        
        # Add some queries
        agent.query("远程办公政策")
        agent.query("VPN配置")
        
        # Clear history
        agent.clear_history()
        
        # Check that history is cleared
        history_summary = agent.get_history_summary()
        assert history_summary['total_messages'] == 0
    
    def test_vector_store_persistence(self, tmp_path):
        """Test that vector store can persist and reload."""
        # Create initial pipeline
        (tmp_path / "test.md").write_text("# Test\nContent")
        
        persist_dir = str(tmp_path / "chroma_db")
        
        pipeline1 = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=persist_dir,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        stats1 = pipeline1.index_documents(verbose=False)
        count1 = stats1['indexed_documents']
        
        # Create new pipeline with same persist directory
        pipeline2 = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=persist_dir,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        # Check that documents are still there
        stats2 = pipeline2.get_pipeline_status()
        assert stats2['collection_count'] >= count1
    
    def test_update_documents(self, tmp_path):
        """Test updating specific documents."""
        # Create initial document
        (tmp_path / "test.md").write_text("# Original\nOriginal content")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        # Index initial document
        stats1 = pipeline.index_documents(verbose=False)
        count1 = stats1['indexed_documents']
        
        # Update document
        (tmp_path / "test.md").write_text("# Updated\nUpdated content")
        
        # Update specific document
        stats2 = pipeline.update_documents(
            [str(tmp_path / "test.md")],
            verbose=False
        )
        
        # Check that document was updated
        assert stats2['loaded_documents'] == 1
        assert stats2['indexed_documents'] >= count1
    
    def test_reindex_all(self, tmp_path):
        """Test re-indexing all documents."""
        # Create documents
        (tmp_path / "test1.md").write_text("# Doc 1\nContent 1")
        (tmp_path / "test2.md").write_text("# Doc 2\nContent 2")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        # Initial index
        stats1 = pipeline.index_documents(verbose=False)
        
        # Re-index
        stats2 = pipeline.reindex_all(verbose=False)
        
        # Check that re-indexing worked
        assert stats2['loaded_documents'] == stats1['loaded_documents']
        assert stats2['indexed_documents'] >= stats1['indexed_documents']
    
    def test_different_search_types(self, indexing_pipeline):
        """Test different search types."""
        # Similarity search
        sim_results = indexing_pipeline.vector_store.similarity_search(
            "远程办公",
            k=2
        )
        assert len(sim_results) == 2
        
        # Search with scores
        score_results = indexing_pipeline.vector_store.similarity_search_with_score(
            "远程办公",
            k=2
        )
        assert len(score_results) == 2
        assert all(isinstance(score, float) for _, score in score_results)
        
        # MMR search
        mmr_results = indexing_pipeline.vector_store.max_marginal_relevance_search(
            "远程办公",
            k=2,
            fetch_k=5,
            lambda_mult=0.5
        )
        assert len(mmr_results) == 2


class TestRAGEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_query(self, tmp_path):
        """Test handling of empty query."""
        (tmp_path / "test.md").write_text("# Test\nContent")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        pipeline.index_documents(verbose=False)
        
        # Empty query should return empty results
        results = pipeline.vector_store.similarity_search("", k=3)
        # Chroma may return some results even for empty query
        assert isinstance(results, list)
    
    def test_no_matching_documents(self, tmp_path):
        """Test query with no matching documents."""
        (tmp_path / "test.md").write_text("# Test\nContent about work")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        pipeline.index_documents(verbose=False)
        
        # Query for something not in documents
        results = pipeline.vector_store.similarity_search(
            "量子物理理论",
            k=3
        )
        
        # Should still return results (based on similarity)
        assert isinstance(results, list)
    
    def test_large_k_value(self, tmp_path):
        """Test retrieval with large k value."""
        (tmp_path / "test.md").write_text("# Test\nContent")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        pipeline.index_documents(verbose=False)
        
        # Request more results than available
        results = pipeline.vector_store.similarity_search("test", k=100)
        
        # Should return all available documents
        assert len(results) <= 100
    
    def test_special_characters_in_query(self, tmp_path):
        """Test query with special characters."""
        (tmp_path / "test.md").write_text("# Test\nContent with special chars: @#$%^&*()")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        pipeline.index_documents(verbose=False)
        
        # Query with special characters
        results = pipeline.vector_store.similarity_search("test @#$%", k=2)
        
        assert isinstance(results, list)
    
    def test_very_long_query(self, tmp_path):
        """Test very long query."""
        (tmp_path / "test.md").write_text("# Test\nContent")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        pipeline.index_documents(verbose=False)
        
        # Very long query
        long_query = "test " * 1000
        results = pipeline.vector_store.similarity_search(long_query, k=2)
        
        assert isinstance(results, list)
