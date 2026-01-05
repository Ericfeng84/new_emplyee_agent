"""
Vector store module for Nexus Agent RAG system.

Provides vector storage and retrieval using Chroma with support for
local persistent storage and in-memory mode.
"""

from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from typing import List, Optional, Dict, Any, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class NexusVectorStore:
    """
    Vector store manager using Chroma.
    
    Supports local persistent storage and in-memory mode.
    Provides similarity search with configurable parameters and metadata filtering.
    """
    
    def __init__(
        self,
        embeddings,
        collection_name: str = "nexus_knowledge_base",
        persist_directory: Optional[str] = None,
    ):
        """
        Initialize the vector store.
        
        Args:
            embeddings: Embeddings model instance (NexusEmbeddings)
            collection_name: Name of the Chroma collection
            persist_directory: Directory for persistent storage (None for in-memory)
        """
        self.embeddings = embeddings
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Initialize Chroma vector store with LangChain 1.0 syntax
        logger.info(f"Initializing Chroma vector store: {collection_name}")
        if persist_directory:
            logger.info(f"Persistent storage: {persist_directory}")
            # Ensure directory exists
            Path(persist_directory).mkdir(parents=True, exist_ok=True)
        else:
            logger.info("Using in-memory storage")
        
        self.vector_store = self._initialize_chroma()
        logger.info("Vector store initialized successfully")
    
    def _initialize_chroma(self) -> VectorStore:
        """
        Initialize Chroma vector store with LangChain 1.0 syntax.
        
        Returns:
            Chroma VectorStore instance
        """
        # Create Chroma vector store with local persistence
        # If persist_directory is None, Chroma will run in-memory
        vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings.get_embeddings_model(),
            persist_directory=self.persist_directory,
        )
        
        return vector_store
    
    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects to add
            ids: Optional list of document IDs
            
        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("No documents to add")
            return []
        
        logger.info(f"Adding {len(documents)} documents to vector store...")
        document_ids = self.vector_store.add_documents(documents=documents, ids=ids)
        logger.info(f"Successfully added {len(document_ids)} documents")
        
        return document_ids
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform similarity search using Chroma.
        
        Args:
            query: Search query text (supports Chinese)
            k: Number of results to return
            filter: Optional metadata filter (Chroma where clause)
            
        Returns:
            List of retrieved Document objects
        """
        logger.debug(f"Searching for: {query[:100]}... (k={k})")
        
        if filter:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
            logger.debug(f"Found {len(results)} results with filter")
        else:
            results = self.vector_store.similarity_search(query=query, k=k)
            logger.debug(f"Found {len(results)} results")
        
        return results
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """
        Perform similarity search with relevance scores.
        
        Args:
            query: Search query text (supports Chinese)
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of tuples (Document, score) where score is distance
        """
        logger.debug(f"Searching with scores for: {query[:100]}... (k={k})")
        
        if filter:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
        else:
            results = self.vector_store.similarity_search_with_score(query=query, k=k)
        
        logger.debug(f"Found {len(results)} results with scores")
        return results
    
    def similarity_search_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform similarity search using an embedding vector.
        
        Args:
            embedding: Query embedding vector
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of retrieved Document objects
        """
        logger.debug(f"Searching by vector (k={k})")
        
        if filter:
            results = self.vector_store.similarity_search_by_vector(
                embedding=embedding,
                k=k,
                filter=filter
            )
        else:
            results = self.vector_store.similarity_search_by_vector(
                embedding=embedding,
                k=k
            )
        
        logger.debug(f"Found {len(results)} results")
        return results
    
    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform maximum marginal relevance search.
        
        This method balances relevance and diversity in results.
        
        Args:
            query: Search query text
            k: Number of results to return
            fetch_k: Number of documents to fetch for MMR
            lambda_mult: Balance between relevance (1.0) and diversity (0.0)
            filter: Optional metadata filter
            
        Returns:
            List of retrieved Document objects
        """
        logger.debug(f"MMR search for: {query[:100]}... (k={k}, fetch_k={fetch_k})")
        
        if filter:
            results = self.vector_store.max_marginal_relevance_search(
                query=query,
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult,
                filter=filter
            )
        else:
            results = self.vector_store.max_marginal_relevance_search(
                query=query,
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult
            )
        
        logger.debug(f"Found {len(results)} MMR results")
        return results
    
    def as_retriever(self, **kwargs) -> "BaseRetriever":
        """
        Get a retriever interface for this vector store.
        
        Args:
            **kwargs: Additional arguments for retriever configuration
                - search_type: 'similarity', 'mmr', or 'similarity_score_threshold'
                - search_kwargs: Dictionary with search parameters (k, score_threshold, etc.)
            
        Returns:
            LangChain Retriever instance
        """
        return self.vector_store.as_retriever(**kwargs)
    
    def delete(
        self,
        ids: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Delete documents from the vector store.
        
        Args:
            ids: List of document IDs to delete
            filter: Metadata filter to select documents to delete
        """
        if ids:
            logger.info(f"Deleting {len(ids)} documents by ID")
            self.vector_store.delete(ids=ids)
        elif filter:
            logger.info(f"Deleting documents with filter: {filter}")
            self.vector_store.delete(where=filter)
        else:
            logger.warning("No IDs or filter provided for deletion")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            # Get the underlying Chroma collection
            collection = self.vector_store._collection
            
            stats = {
                'name': collection.name,
                'count': collection.count(),
                'metadata': collection.metadata,
            }
            
            logger.info(f"Collection stats: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {
                'name': self.collection_name,
                'count': 0,
                'error': str(e),
            }
    
    def clear_collection(self) -> None:
        """
        Clear all documents from the collection.
        
        Warning: This operation is irreversible.
        """
        logger.warning(f"Clearing all documents from collection: {self.collection_name}")
        
        # Delete all documents
        self.vector_store.delete(where={})
        
        logger.info("Collection cleared successfully")
    
    def persist(self) -> None:
        """
        Persist the vector store to disk.
        
        Only applicable when using persistent storage.
        """
        if self.persist_directory:
            logger.info(f"Persisting vector store to: {self.persist_directory}")
            # Chroma automatically persists, but we can ensure it's flushed
            if hasattr(self.vector_store, 'persist'):
                self.vector_store.persist()
            logger.info("Vector store persisted")
        else:
            logger.warning("Cannot persist: using in-memory storage")
