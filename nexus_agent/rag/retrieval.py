"""
Retrieval module for Nexus Agent RAG system.

Provides advanced retrieval capabilities including similarity search,
re-ranking, and hybrid retrieval strategies.
"""

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from typing import List, Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class NexusRetriever(BaseRetriever):
    """
    Advanced retriever with multiple strategies for Nexus RAG system.
    
    Supports:
    - Similarity search
    - Maximum marginal relevance (MMR)
    - Similarity with score threshold
    - Hybrid retrieval
    """
    
    def __init__(
        self,
        vector_store,
        search_type: str = "similarity",
        search_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize the retriever.
        
        Args:
            vector_store: VectorStore instance (NexusVectorStore)
            search_type: Type of search ('similarity', 'mmr', 'similarity_score_threshold')
            search_kwargs: Additional search parameters (k, score_threshold, fetch_k, lambda_mult)
            **kwargs: Additional arguments for BaseRetriever
        """
        self.vector_store = vector_store
        self.search_type = search_type
        self.search_kwargs = search_kwargs or {}
        super().__init__(**kwargs)
        
        logger.info(
            f"Retriever initialized: search_type={search_type}, "
            f"search_kwargs={search_kwargs}"
        )
    
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
        """
        Retrieve relevant documents based on the query.
        
        Args:
            query: Search query text (supports Chinese)
            run_manager: Callback manager for this retrieval run
            
        Returns:
            List of relevant Document objects
        """
        logger.debug(f"Retrieving documents for query: {query[:100]}...")
        
        k = self.search_kwargs.get('k', 4)
        filter = self.search_kwargs.get('filter', None)
        
        if self.search_type == "similarity":
            # Standard similarity search
            docs = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
        
        elif self.search_type == "mmr":
            # Maximum marginal relevance search
            fetch_k = self.search_kwargs.get('fetch_k', 20)
            lambda_mult = self.search_kwargs.get('lambda_mult', 0.5)
            
            docs = self.vector_store.max_marginal_relevance_search(
                query=query,
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult,
                filter=filter
            )
        
        elif self.search_type == "similarity_score_threshold":
            # Similarity search with score threshold
            score_threshold = self.search_kwargs.get('score_threshold', 0.7)
            
            results_with_scores = self.vector_store.similarity_search_with_score(
                query=query,
                k=k * 2,  # Fetch more to filter by threshold
                filter=filter
            )
            
            # Filter by score threshold (lower is better for distance)
            docs = [
                doc for doc, score in results_with_scores
                if score <= (1.0 - score_threshold)  # Convert to distance
            ][:k]
        
        else:
            raise ValueError(f"Unknown search type: {self.search_type}")
        
        logger.debug(f"Retrieved {len(docs)} documents")
        return docs


class HybridRetriever:
    """
    Hybrid retriever that combines multiple retrieval strategies.
    
    Can combine results from different retrievers and apply re-ranking.
    """
    
    def __init__(
        self,
        retrievers: List[BaseRetriever],
        weights: Optional[List[float]] = None,
        top_k: int = 5,
    ):
        """
        Initialize the hybrid retriever.
        
        Args:
            retrievers: List of retriever instances to combine
            weights: Optional weights for each retriever (must sum to 1.0)
            top_k: Number of top results to return
        """
        self.retrievers = retrievers
        self.top_k = top_k
        
        if weights is None:
            # Equal weights for all retrievers
            self.weights = [1.0 / len(retrievers)] * len(retrievers)
        else:
            if len(weights) != len(retrievers):
                raise ValueError("Number of weights must match number of retrievers")
            if abs(sum(weights) - 1.0) > 0.01:
                raise ValueError("Weights must sum to 1.0")
            self.weights = weights
        
        logger.info(
            f"Hybrid retriever initialized with {len(retrievers)} retrievers, "
            f"weights={self.weights}"
        )
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents using hybrid approach.
        
        Args:
            query: Search query text
            
        Returns:
            List of relevant Document objects
        """
        logger.debug(f"Hybrid retrieval for query: {query[:100]}...")
        
        # Retrieve documents from each retriever
        all_results = []
        for i, retriever in enumerate(retriever := self.retrievers):
            docs = retriever.invoke(query)
            weight = self.weights[i]
            
            for doc in docs:
                # Add weight to metadata for re-ranking
                doc.metadata['retriever_weight'] = weight
                doc.metadata['retriever_index'] = i
                all_results.append(doc)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_docs = []
        for doc in all_results:
            # Use content and source as unique identifier
            identifier = (doc.page_content, doc.metadata.get('source', ''))
            if identifier not in seen:
                seen.add(identifier)
                unique_docs.append(doc)
        
        # Return top_k results
        results = unique_docs[:self.top_k]
        logger.debug(f"Hybrid retrieval returned {len(results)} documents")
        
        return results
    
    def add_retriever(
        self,
        retriever: BaseRetriever,
        weight: Optional[float] = None
    ) -> None:
        """
        Add a new retriever to the hybrid retriever.
        
        Args:
            retriever: Retriever instance to add
            weight: Weight for this retriever (defaults to equal distribution)
        """
        self.retrievers.append(retriever)
        
        if weight is not None:
            self.weights.append(weight)
        else:
            # Redistribute weights equally
            self.weights = [1.0 / len(self.retrievers)] * len(self.retrievers)
        
        logger.info(f"Added retriever, total retrievers: {len(self.retrievers)}")


class ContextualRetriever:
    """
    Retriever that considers conversation context for retrieval.
    
    Maintains a history of queries and uses them to improve retrieval.
    """
    
    def __init__(
        self,
        base_retriever: BaseRetriever,
        context_window: int = 3,
    ):
        """
        Initialize the contextual retriever.
        
        Args:
            base_retriever: Base retriever to wrap
            context_window: Number of previous queries to consider
        """
        self.base_retriever = base_retriever
        self.context_window = context_window
        self.query_history: List[str] = []
        
        logger.info(
            f"Contextual retriever initialized with context_window={context_window}"
        )
    
    def get_relevant_documents(
        self,
        query: str,
        use_context: bool = True
    ) -> List[Document]:
        """
        Retrieve relevant documents with context awareness.
        
        Args:
            query: Search query text
            use_context: Whether to use query history for context
            
        Returns:
            List of relevant Document objects
        """
        logger.debug(f"Contextual retrieval for query: {query[:100]}...")
        
        # Add current query to history
        self.query_history.append(query)
        
        # Keep only recent queries
        if len(self.query_history) > self.context_window:
            self.query_history = self.query_history[-self.context_window:]
        
        if use_context and len(self.query_history) > 1:
            # Combine recent queries for better context
            context_query = " ".join(self.query_history)
            logger.debug(f"Using context with {len(self.query_history)} queries")
        else:
            context_query = query
        
        # Retrieve using base retriever
        docs = self.base_retriever.invoke(context_query)
        
        # Add context metadata
        for doc in docs:
            doc.metadata['context_queries'] = len(self.query_history)
        
        logger.debug(f"Contextual retrieval returned {len(docs)} documents")
        return docs
    
    def clear_history(self) -> None:
        """Clear the query history."""
        self.query_history.clear()
        logger.info("Query history cleared")


def create_retriever(
    vector_store,
    search_type: str = "similarity",
    k: int = 4,
    score_threshold: Optional[float] = None,
    fetch_k: int = 20,
    lambda_mult: float = 0.5,
    filter: Optional[Dict[str, Any]] = None,
) -> BaseRetriever:
    """
    Factory function to create a configured retriever.
    
    Args:
        vector_store: VectorStore instance
        search_type: Type of search ('similarity', 'mmr', 'similarity_score_threshold')
        k: Number of results to return
        score_threshold: Minimum similarity score (0-1)
        fetch_k: Number of documents to fetch for MMR
        lambda_mult: Balance between relevance (1.0) and diversity (0.0) for MMR
        filter: Optional metadata filter
        
    Returns:
        Configured NexusRetriever instance
    """
    search_kwargs = {'k': k}
    
    if score_threshold is not None:
        search_kwargs['score_threshold'] = score_threshold
    
    if fetch_k is not None:
        search_kwargs['fetch_k'] = fetch_k
    
    if lambda_mult is not None:
        search_kwargs['lambda_mult'] = lambda_mult
    
    if filter is not None:
        search_kwargs['filter'] = filter
    
    return NexusRetriever(
        vector_store=vector_store,
        search_type=search_type,
        search_kwargs=search_kwargs
    )
