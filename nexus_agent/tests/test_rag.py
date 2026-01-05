"""
Unit tests for RAG components.

Tests document loading, text splitting, embeddings, vector store,
and retrieval functionality.
"""

import pytest
from langchain_core.documents import Document
from nexus_agent.rag.document_loader import NexusDocumentLoader
from nexus_agent.rag.text_splitter import NexusTextSplitter
from nexus_agent.rag.embeddings import NexusEmbeddings
from nexus_agent.rag.vector_store import NexusVectorStore
from nexus_agent.rag.indexing import NexusIndexingPipeline
from nexus_agent.rag.retrieval import NexusRetriever, create_retriever
from nexus_agent.utils.data_preprocessing import DataPreprocessor


class TestDocumentLoader:
    """Tests for NexusDocumentLoader."""
    
    def test_loader_initialization(self):
        """Test document loader initialization."""
        loader = NexusDocumentLoader()
        assert loader.data_dir is not None
        assert len(loader.supported_formats) > 0
    
    def test_load_markdown_document(self, tmp_path):
        """Test loading markdown document."""
        # Create test markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\n\nThis is a test document.")
        
        loader = NexusDocumentLoader(data_dir=str(tmp_path))
        docs = loader.load_documents([str(test_file)])
        
        assert len(docs) > 0
        assert "Test Document" in docs[0].page_content
        assert docs[0].metadata['file_type'] == '.md'
        assert docs[0].metadata['file_name'] == 'test.md'
    
    def test_load_text_document(self, tmp_path):
        """Test loading text document."""
        # Create test text file
        test_file = tmp_path / "test.txt"
        test_file.write_text("This is a plain text document.")
        
        loader = NexusDocumentLoader(data_dir=str(tmp_path))
        docs = loader.load_documents([str(test_file)])
        
        assert len(docs) > 0
        assert "plain text document" in docs[0].page_content
        assert docs[0].metadata['file_type'] == '.txt'
    
    def test_load_all_documents(self, tmp_path):
        """Test loading all documents from directory."""
        # Create multiple test files
        (tmp_path / "test1.md").write_text("# Doc 1\nContent 1")
        (tmp_path / "test2.txt").write_text("Content 2")
        (tmp_path / "test3.md").write_text("# Doc 3\nContent 3")
        
        loader = NexusDocumentLoader(data_dir=str(tmp_path))
        docs = loader.load_documents()
        
        assert len(docs) == 3
    
    def test_metadata_preservation(self, tmp_path):
        """Test that document metadata is preserved."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\nContent")
        
        loader = NexusDocumentLoader(data_dir=str(tmp_path))
        docs = loader.load_documents([str(test_file)])
        
        assert 'source' in docs[0].metadata
        assert 'file_type' in docs[0].metadata
        assert 'file_name' in docs[0].metadata
        assert 'file_size' in docs[0].metadata
    
    def test_get_document_stats(self, tmp_path):
        """Test getting document statistics."""
        (tmp_path / "test1.md").write_text("# Doc 1\nContent 1")
        (tmp_path / "test2.txt").write_text("Content 2")
        
        loader = NexusDocumentLoader(data_dir=str(tmp_path))
        docs = loader.load_documents()
        stats = loader.get_document_stats(docs)
        
        assert stats['total_documents'] == 2
        assert stats['total_characters'] > 0
        assert 'file_types' in stats


class TestTextSplitter:
    """Tests for NexusTextSplitter."""
    
    def test_recursive_splitter_initialization(self):
        """Test recursive splitter initialization."""
        splitter = NexusTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            strategy="recursive"
        )
        assert splitter.chunk_size == 500
        assert splitter.chunk_overlap == 100
        assert splitter.strategy == "recursive"
    
    def test_markdown_splitter_initialization(self):
        """Test markdown splitter initialization."""
        splitter = NexusTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            strategy="markdown"
        )
        assert splitter.strategy == "markdown"
    
    def test_split_documents(self):
        """Test splitting documents into chunks."""
        splitter = NexusTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            strategy="recursive"
        )
        
        # Create a long document
        test_doc = Document(
            page_content="A" * 1000,
            metadata={'file_type': '.txt'}
        )
        
        splits = splitter.split_documents([test_doc])
        
        assert len(splits) > 1
        assert all(len(split.page_content) <= 600 for split in splits)
    
    def test_split_markdown_document(self):
        """Test splitting markdown document."""
        splitter = NexusTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            strategy="recursive"
        )
        
        # Create markdown document
        test_doc = Document(
            page_content="# Header 1\nContent 1\n\n# Header 2\nContent 2\n\n" + "A" * 1000,
            metadata={'file_type': '.md'}
        )
        
        splits = splitter.split_documents([test_doc])
        
        assert len(splits) > 1
    
    def test_split_text(self):
        """Test splitting text string."""
        splitter = NexusTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        
        text = "A" * 1000
        chunks = splitter.split_text(text)
        
        assert len(chunks) > 1
        assert all(len(chunk) <= 600 for chunk in chunks)
    
    def test_get_split_stats(self):
        """Test getting splitting statistics."""
        splitter = NexusTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        test_docs = [
            Document(page_content="A" * 2000, metadata={'file_type': '.txt'}),
            Document(page_content="B" * 1500, metadata={'file_type': '.txt'})
        ]
        
        stats = splitter.get_split_stats(test_docs)
        
        assert stats['total_documents'] == 2
        assert stats['total_chunks'] > 2
        assert stats['average_chunk_size'] > 0
        assert 'chunk_size_range' in stats


class TestEmbeddings:
    """Tests for NexusEmbeddings."""
    
    def test_embeddings_initialization(self):
        """Test embeddings model initialization."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        assert embeddings.model_name == "BAAI/bge-small-zh-v1.5"
        assert embeddings.device == "cpu"
        assert embeddings.normalize_embeddings == True
    
    def test_embed_query(self):
        """Test embedding a single query."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        query = "这是一个测试查询"
        embedding = embeddings.embed_query(query)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embed_documents(self):
        """Test embedding multiple documents."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        texts = ["文档一", "文档二", "文档三"]
        embeddings_list = embeddings.embed_documents(texts)
        
        assert len(embeddings_list) == 3
        assert all(len(emb) > 0 for emb in embeddings_list)
    
    def test_get_embedding_dimension(self):
        """Test getting embedding dimension."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        dimension = embeddings.get_embedding_dimension()
        
        assert dimension > 0
        assert isinstance(dimension, int)
    
    def test_compute_similarity(self):
        """Test computing similarity between embeddings."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        emb1 = embeddings.embed_query("测试文本一")
        emb2 = embeddings.embed_query("测试文本二")
        
        similarity = embeddings.compute_similarity(emb1, emb2)
        
        assert 0 <= similarity <= 1
        assert isinstance(similarity, float)


class TestVectorStore:
    """Tests for NexusVectorStore."""
    
    def test_vector_store_initialization(self):
        """Test vector store initialization."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        # Use in-memory store for testing
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        assert vector_store.collection_name == "nexus_knowledge_base"
        assert vector_store.persist_directory is None
    
    def test_add_documents(self):
        """Test adding documents to vector store."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        test_docs = [
            Document(page_content="公司远程办公政策"),
            Document(page_content="IT支持VPN配置"),
            Document(page_content="员工福利和津贴")
        ]
        
        doc_ids = vector_store.add_documents(test_docs)
        
        assert len(doc_ids) == 3
    
    def test_similarity_search(self):
        """Test similarity search with Chinese text."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        # Add test documents
        test_docs = [
            Document(page_content="公司远程办公政策"),
            Document(page_content="IT支持VPN配置"),
            Document(page_content="员工福利和津贴")
        ]
        vector_store.add_documents(test_docs)
        
        # Search with Chinese query
        results = vector_store.similarity_search("远程办公政策", k=2)
        
        assert len(results) == 2
        assert any("远程" in doc.page_content for doc in results)
    
    def test_similarity_search_with_score(self):
        """Test similarity search with scores."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        test_docs = [
            Document(page_content="HR政策"),
            Document(page_content="IT政策")
        ]
        vector_store.add_documents(test_docs)
        
        results = vector_store.similarity_search_with_score("政策", k=2)
        
        assert len(results) == 2
        assert all(isinstance(score, float) for _, score in results)
    
    def test_max_marginal_relevance_search(self):
        """Test maximum marginal relevance search."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        test_docs = [
            Document(page_content="文档一"),
            Document(page_content="文档二"),
            Document(page_content="文档三")
        ]
        vector_store.add_documents(test_docs)
        
        results = vector_store.max_marginal_relevance_search(
            "文档",
            k=2,
            fetch_k=3,
            lambda_mult=0.5
        )
        
        assert len(results) == 2
    
    def test_get_collection_stats(self):
        """Test getting collection statistics."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        test_docs = [
            Document(page_content="测试文档")
        ]
        vector_store.add_documents(test_docs)
        
        stats = vector_store.get_collection_stats()
        
        assert 'name' in stats
        assert 'count' in stats
        assert stats['count'] >= 1


class TestRetriever:
    """Tests for NexusRetriever."""
    
    def test_retriever_creation(self):
        """Test creating a retriever."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        retriever = create_retriever(
            vector_store,
            search_type="similarity",
            k=3
        )
        
        assert retriever.search_type == "similarity"
        assert retriever.search_kwargs['k'] == 3
    
    def test_retriever_invoke(self):
        """Test invoking retriever."""
        embeddings = NexusEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            device="cpu"
        )
        
        vector_store = NexusVectorStore(
            embeddings=embeddings,
            persist_directory=None
        )
        
        test_docs = [
            Document(page_content="公司远程办公政策"),
            Document(page_content="IT支持VPN配置")
        ]
        vector_store.add_documents(test_docs)
        
        retriever = create_retriever(vector_store, k=2)
        results = retriever.invoke("远程办公")
        
        assert len(results) > 0
        assert isinstance(results[0], Document)


class TestDataPreprocessor:
    """Tests for DataPreprocessor."""
    
    def test_clean_text(self):
        """Test text cleaning."""
        text = "This  is  a  test  \n\nwith  extra  spaces."
        cleaned = DataPreprocessor.clean_text(text)
        
        assert "  " not in cleaned
        assert "\n\n" not in cleaned
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        text = "This   has    multiple     spaces"
        normalized = DataPreprocessor.normalize_whitespace(text)
        
        assert "   " not in normalized
        assert " " in normalized
    
    def test_remove_urls(self):
        """Test URL removal."""
        text = "Visit https://example.com for more info"
        cleaned = DataPreprocessor.remove_urls(text)
        
        assert "https://" not in cleaned
    
    def test_remove_email_addresses(self):
        """Test email address removal."""
        text = "Contact us at test@example.com"
        cleaned = DataPreprocessor.remove_email_addresses(text)
        
        assert "@" not in cleaned
    
    def test_extract_tables(self):
        """Test table extraction."""
        text = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
"""
        tables = DataPreprocessor.extract_tables(text)
        
        assert len(tables) == 1
        assert 'header' in tables[0]
        assert 'rows' in tables[0]
    
    def test_format_table_as_text(self):
        """Test formatting table as text."""
        table = {
            'header': ['Name', 'Age'],
            'rows': [['Alice', '25'], ['Bob', '30']]
        }
        
        formatted = DataPreprocessor.format_table_as_text(table)
        
        assert '表格:' in formatted
        assert 'Name' in formatted
        assert 'Age' in formatted
    
    def test_extract_code_blocks(self):
        """Test code block extraction."""
        text = """
```python
def hello():
    print("Hello, World!")
```
"""
        code_blocks = DataPreprocessor.extract_code_blocks(text)
        
        assert len(code_blocks) == 1
        assert code_blocks[0]['language'] == 'python'
        assert 'def hello' in code_blocks[0]['code']
    
    def test_extract_headings(self):
        """Test heading extraction."""
        text = """
# Heading 1
Content 1

## Heading 2
Content 2

### Heading 3
Content 3
"""
        headings = DataPreprocessor.extract_headings(text)
        
        assert len(headings) == 3
        assert headings[0]['level'] == 1
        assert headings[1]['level'] == 2
        assert headings[2]['level'] == 3
    
    def test_detect_language(self):
        """Test language detection."""
        chinese_text = "这是一段中文文本"
        english_text = "This is English text"
        mixed_text = "This is mixed 中英文文本"
        
        assert DataPreprocessor.detect_language(chinese_text) == 'zh'
        assert DataPreprocessor.detect_language(english_text) == 'en'
        assert DataPreprocessor.detect_language(mixed_text) == 'mixed'
    
    def test_preprocess_document(self):
        """Test document preprocessing."""
        text = "Test  document  with  extra  spaces"
        processed = DataPreprocessor.preprocess_document(
            text,
            clean=True,
            normalize=True
        )
        
        assert "  " not in processed


class TestIndexingPipeline:
    """Tests for NexusIndexingPipeline."""
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization."""
        pipeline = NexusIndexingPipeline(
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        assert pipeline.chunk_size == 1000
        assert pipeline.chunk_overlap == 200
    
    def test_index_documents(self, tmp_path):
        """Test complete indexing pipeline."""
        # Create test documents
        (tmp_path / "test1.md").write_text("# Doc 1\nContent 1")
        (tmp_path / "test2.txt").write_text("Content 2")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        stats = pipeline.index_documents(verbose=False)
        
        assert stats['loaded_documents'] > 0
        assert stats['total_chunks'] > 0
        assert stats['indexed_documents'] > 0
    
    def test_test_retrieval(self, tmp_path):
        """Test retrieval after indexing."""
        # Create test document
        (tmp_path / "test.md").write_text("# 远程办公\n公司支持远程办公")
        
        pipeline = NexusIndexingPipeline(
            data_dir=str(tmp_path),
            persist_directory=None,
            embedding_model="BAAI/bge-small-zh-v1.5"
        )
        
        pipeline.index_documents(verbose=False)
        results = pipeline.test_retrieval("远程办公", k=1, verbose=False)
        
        assert len(results) > 0
        assert "远程办公" in results[0].page_content
