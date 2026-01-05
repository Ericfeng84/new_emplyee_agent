"""
Indexing pipeline module for Nexus Agent RAG system.

Provides complete ETL pipeline for document indexing:
Load -> Split -> Embed -> Store
"""

from .document_loader import NexusDocumentLoader
from .text_splitter import NexusTextSplitter
from .embeddings import NexusEmbeddings
from .vector_store import NexusVectorStore
from langchain_core.documents import Document
from typing import List, Optional, Dict, Any
import logging
import time

logger = logging.getLogger(__name__)


class NexusIndexingPipeline:
    """
    Complete ETL pipeline for document indexing.
    
    Orchestrates the entire indexing process:
    1. Load documents from files
    2. Split documents into chunks
    3. Generate embeddings
    4. Store in vector database
    """
    
    def __init__(
        self,
        data_dir: str = "nexus_agent/data/documents",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        embedding_model: str = "BAAI/bge-small-zh-v1.5",
        embedding_device: str = "cpu",
        persist_directory: Optional[str] = "nexus_agent/data/chroma_db",
        collection_name: str = "nexus_knowledge_base",
    ):
        """
        Initialize the indexing pipeline.
        
        Args:
            data_dir: Directory containing documents to index
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks
            embedding_model: Name of the BGE embedding model
            embedding_device: Device for embedding generation
            persist_directory: Directory for vector store persistence
            collection_name: Name of the Chroma collection
        """
        self.data_dir = data_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.embedding_device = embedding_device
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize components
        self.loader = NexusDocumentLoader(data_dir=data_dir)
        self.splitter = NexusTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embeddings = NexusEmbeddings(
            model_name=embedding_model,
            device=embedding_device
        )
        self.vector_store = NexusVectorStore(
            embeddings=self.embeddings,
            collection_name=collection_name,
            persist_directory=persist_directory
        )
        
        logger.info("Indexing pipeline initialized successfully")
    
    def index_documents(
        self,
        file_paths: Optional[List[str]] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run complete indexing pipeline.
        
        Args:
            file_paths: Specific file paths to index, or None for all documents
            verbose: Whether to print progress information
            
        Returns:
            Dictionary with indexing statistics
        """
        start_time = time.time()
        stats = {
            'start_time': start_time,
            'file_paths': file_paths,
        }
        
        if verbose:
            print("=" * 60)
            print("Nexus Document Indexing Pipeline")
            print("=" * 60)
        
        # Step 1: Load documents
        if verbose:
            print("\n📄 Step 1: Loading documents...")
        
        docs = self.loader.load_documents(file_paths)
        stats['loaded_documents'] = len(docs)
        
        if verbose:
            print(f"   ✓ Loaded {len(docs)} document(s)")
            
            # Show document stats
            doc_stats = self.loader.get_document_stats(docs)
            print(f"   - Total characters: {doc_stats['total_characters']:,}")
            print(f"   - File types: {', '.join(doc_stats['file_types'].keys())}")
        
        if not docs:
            logger.warning("No documents loaded, aborting indexing")
            if verbose:
                print("\n⚠️  No documents found to index")
            return stats
        
        # Step 2: Split documents
        if verbose:
            print("\n✂️  Step 2: Splitting documents into chunks...")
        
        splits = self.splitter.split_documents(docs)
        stats['total_chunks'] = len(splits)
        
        if verbose:
            print(f"   ✓ Created {len(splits)} chunk(s)")
        
        # Get splitting statistics
        split_stats = self.splitter.get_split_stats(docs)
        stats.update(split_stats)
        
        if verbose:
            print(f"   - Average chunk size: {split_stats['average_chunk_size']:.0f} characters")
            print(f"   - Chunk size range: {split_stats['chunk_size_range'][0]} - {split_stats['chunk_size_range'][1]} characters")
            print(f"   - Chunks per document: {split_stats['chunks_per_document']:.1f}")
        
        # Step 3: Add to vector store
        if verbose:
            print("\n🔢 Step 3: Generating embeddings and storing in vector database...")
        
        document_ids = self.vector_store.add_documents(splits)
        stats['indexed_documents'] = len(document_ids)
        
        if verbose:
            print(f"   ✓ Indexed {len(document_ids)} chunk(s)")
        
        # Get collection stats
        collection_stats = self.vector_store.get_collection_stats()
        stats['collection_stats'] = collection_stats
        
        if verbose:
            print(f"   - Total documents in collection: {collection_stats['count']}")
        
        # Calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        stats['elapsed_time'] = elapsed_time
        stats['end_time'] = end_time
        
        if verbose:
            print("\n✅ Indexing completed successfully!")
            print("\n📊 Summary:")
            print(f"   - Documents loaded: {stats['loaded_documents']}")
            print(f"   - Chunks created: {stats['total_chunks']}")
            print(f"   - Chunks indexed: {stats['indexed_documents']}")
            print(f"   - Average chunk size: {stats['average_chunk_size']:.0f} characters")
            print(f"   - Total time: {elapsed_time:.2f} seconds")
            print(f"   - Processing rate: {stats['total_chunks'] / elapsed_time:.1f} chunks/second")
            print("=" * 60)
        
        logger.info(
            f"Indexing completed: {stats['loaded_documents']} docs -> "
            f"{stats['total_chunks']} chunks -> {stats['indexed_documents']} indexed "
            f"in {elapsed_time:.2f}s"
        )
        
        return stats
    
    def reindex_all(
        self,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Re-index all documents (clears existing index).
        
        Args:
            verbose: Whether to print progress information
            
        Returns:
            Dictionary with indexing statistics
        """
        if verbose:
            print("\n🔄 Re-indexing all documents...")
            print("   Clearing existing index...")
        
        # Clear the collection
        self.vector_store.clear_collection()
        
        # Re-index all documents
        return self.index_documents(verbose=verbose)
    
    def update_documents(
        self,
        file_paths: List[str],
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Update specific documents in the index.
        
        This method deletes existing chunks from the specified files
        and re-indexes them.
        
        Args:
            file_paths: List of file paths to update
            verbose: Whether to print progress information
            
        Returns:
            Dictionary with indexing statistics
        """
        if verbose:
            print(f"\n🔄 Updating {len(file_paths)} document(s)...")
        
        # Delete existing chunks for these files
        for file_path in file_paths:
            # Use file_name as filter
            from pathlib import Path
            file_name = Path(file_path).name
            self.vector_store.delete(filter={"file_name": file_name})
            
            if verbose:
                print(f"   ✓ Deleted existing chunks for {file_name}")
        
        # Index the updated documents
        return self.index_documents(file_paths=file_paths, verbose=verbose)
    
    def test_retrieval(
        self,
        query: str,
        k: int = 3,
        verbose: bool = True
    ) -> List[Document]:
        """
        Test retrieval from the indexed documents.
        
        Args:
            query: Test query (supports Chinese)
            k: Number of results to retrieve
            verbose: Whether to print results
            
        Returns:
            List of retrieved Document objects
        """
        if verbose:
            print(f"\n🔍 Testing retrieval with query: {query}")
        
        results = self.vector_store.similarity_search(query, k=k)
        
        if verbose:
            print(f"   Found {len(results)} result(s):\n")
            for i, doc in enumerate(results, 1):
                print(f"   Result {i}:")
                print(f"   - Source: {doc.metadata.get('file_name', 'Unknown')}")
                print(f"   - Content: {doc.page_content[:200]}...")
                print()
        
        return results
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get the current status of the indexing pipeline.
        
        Returns:
            Dictionary with pipeline status information
        """
        collection_stats = self.vector_store.get_collection_stats()
        
        return {
            'data_directory': self.data_dir,
            'collection_name': self.collection_name,
            'persist_directory': self.persist_directory,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'embedding_model': self.embedding_model,
            'embedding_device': self.embedding_device,
            'collection_count': collection_stats.get('count', 0),
            'collection_metadata': collection_stats.get('metadata', {}),
        }
