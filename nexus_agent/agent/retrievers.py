"""
Retrievers module for Nexus Agent.

Provides retriever configurations and utilities for the RAG system.
"""

from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class NexusRetrieverConfig:
    """
    Configuration class for Nexus retrievers.
    
    Provides predefined configurations for common retrieval scenarios.
    """
    
    @staticmethod
    def default_config() -> Dict[str, Any]:
        """
        Default retrieval configuration.
        
        Returns:
            Dictionary with default retrieval parameters
        """
        return {
            'search_type': 'similarity',
            'k': 4,
        }
    
    @staticmethod
    def high_precision_config() -> Dict[str, Any]:
        """
        High precision retrieval configuration.
        
        Uses fewer but more relevant results.
        
        Returns:
            Dictionary with high precision parameters
        """
        return {
            'search_type': 'similarity',
            'k': 3,
        }
    
    @staticmethod
    def high_recall_config() -> Dict[str, Any]:
        """
        High recall retrieval configuration.
        
        Retrieves more results for comprehensive coverage.
        
        Returns:
            Dictionary with high recall parameters
        """
        return {
            'search_type': 'similarity',
            'k': 10,
        }
    
    @staticmethod
    def diverse_results_config() -> Dict[str, Any]:
        """
        Diverse results retrieval configuration.
        
        Uses MMR to get diverse, relevant results.
        
        Returns:
            Dictionary with MMR parameters
        """
        return {
            'search_type': 'mmr',
            'k': 5,
            'fetch_k': 20,
            'lambda_mult': 0.5,
        }
    
    @staticmethod
    def thresholded_config(score_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Thresholded retrieval configuration.
        
        Only returns results above a similarity threshold.
        
        Args:
            score_threshold: Minimum similarity score (0-1)
            
        Returns:
            Dictionary with thresholded parameters
        """
        return {
            'search_type': 'similarity_score_threshold',
            'k': 10,
            'score_threshold': score_threshold,
        }


class MetadataFilterRetriever(BaseRetriever):
    """
    Retriever with metadata filtering capabilities.
    
    Allows filtering results by metadata fields such as
    file type, source, or custom metadata.
    """
    
    def __init__(
        self,
        base_retriever: BaseRetriever,
        metadata_filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize the metadata filter retriever.
        
        Args:
            base_retriever: Base retriever to wrap
            metadata_filter: Metadata filter to apply
            **kwargs: Additional arguments for BaseRetriever
        """
        self.base_retriever = base_retriever
        self.metadata_filter = metadata_filter or {}
        super().__init__(**kwargs)
        
        logger.info(
            f"Metadata filter retriever initialized with filter: {metadata_filter}"
        )
    
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
        """
        Retrieve relevant documents with metadata filtering.
        
        Args:
            query: Search query text
            run_manager: Callback manager for this retrieval run
            
        Returns:
            List of filtered Document objects
        """
        logger.debug(f"Retrieving with metadata filter: {self.metadata_filter}")
        
        # Get documents from base retriever
        docs = self.base_retriever.invoke(query)
        
        # Apply metadata filter
        if self.metadata_filter:
            filtered_docs = [
                doc for doc in docs
                if all(
                    doc.metadata.get(key) == value
                    for key, value in self.metadata_filter.items()
                )
            ]
            
            logger.debug(
                f"Filtered {len(docs)} documents to {len(filtered_docs)}"
            )
            return filtered_docs
        
        return docs
    
    def update_filter(self, metadata_filter: Dict[str, Any]) -> None:
        """
        Update the metadata filter.
        
        Args:
            metadata_filter: New metadata filter to apply
        """
        self.metadata_filter = metadata_filter
        logger.info(f"Updated metadata filter: {metadata_filter}")


class CompositeRetriever(BaseRetriever):
    """
    Composite retriever that combines multiple retrievers.
    
    Retrieves from multiple sources and merges results.
    """
    
    def __init__(
        self,
        retrievers: List[BaseRetriever],
        merge_strategy: str = "union",
        **kwargs
    ):
        """
        Initialize the composite retriever.
        
        Args:
            retrievers: List of retriever instances to combine
            merge_strategy: How to merge results ('union', 'intersection', 'weighted')
            **kwargs: Additional arguments for BaseRetriever
        """
        self.retrievers = retrievers
        self.merge_strategy = merge_strategy
        super().__init__(**kwargs)
        
        logger.info(
            f"Composite retriever initialized with {len(retrievers)} retrievers, "
            f"merge_strategy={merge_strategy}"
        )
    
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
        """
        Retrieve relevant documents from all retrievers.
        
        Args:
            query: Search query text
            run_manager: Callback manager for this retrieval run
            
        Returns:
            List of merged Document objects
        """
        logger.debug(f"Composite retrieval for query: {query[:100]}...")
        
        # Retrieve from all retrievers
        all_results = []
        for i, retriever in enumerate(self.retrievers):
            docs = retriever.invoke(query)
            
            # Add retriever index to metadata
            for doc in docs:
                doc.metadata['retriever_index'] = i
            
            all_results.extend(docs)
        
        # Merge based on strategy
        if self.merge_strategy == "union":
            # Union: all unique documents
            results = self._deduplicate(all_results)
        
        elif self.merge_strategy == "intersection":
            # Intersection: documents found by all retrievers
            results = self._intersect(all_results, len(self.retrievers))
        
        else:
            raise ValueError(f"Unknown merge strategy: {self.merge_strategy}")
        
        logger.debug(f"Composite retrieval returned {len(results)} documents")
        return results
    
    def _deduplicate(self, documents: List[Document]) -> List[Document]:
        """
        Remove duplicate documents based on content.
        
        Args:
            documents: List of documents to deduplicate
            
        Returns:
            List of unique documents
        """
        seen = set()
        unique_docs = []
        
        for doc in documents:
            # Use content and source as unique identifier
            identifier = (doc.page_content, doc.metadata.get('source', ''))
            if identifier not in seen:
                seen.add(identifier)
                unique_docs.append(doc)
        
        return unique_docs
    
    def _intersect(
        self,
        documents: List[Document],
        num_retrievers: int
    ) -> List[Document]:
        """
        Find documents that appear in all retriever results.
        
        Args:
            documents: List of documents from all retrievers
            num_retrievers: Number of retrievers
            
        Returns:
            List of documents found by all retrievers
        """
        # Count occurrences of each document
        doc_counts = {}
        
        for doc in documents:
            identifier = (doc.page_content, doc.metadata.get('source', ''))
            if identifier not in doc_counts:
                doc_counts[identifier] = []
            doc_counts[identifier].append(doc)
        
        # Keep only documents found by all retrievers
        intersection = []
        seen = set()
        
        for doc in documents:
            identifier = (doc.page_content, doc.metadata.get('source', ''))
            if len(doc_counts[identifier]) == num_retrievers and identifier not in seen:
                intersection.append(doc)
                seen.add(identifier)
        
        return intersection


def create_retriever_from_config(
    vector_store,
    config_name: str = "default",
    **kwargs
) -> BaseRetriever:
    """
    Create a retriever from a predefined configuration.
    
    Args:
        vector_store: VectorStore instance
        config_name: Name of the configuration ('default', 'high_precision', etc.)
        **kwargs: Additional parameters to override config
        
    Returns:
        Configured retriever instance
    """
    # Get configuration
    config_map = {
        'default': NexusRetrieverConfig.default_config(),
        'high_precision': NexusRetrieverConfig.high_precision_config(),
        'high_recall': NexusRetrieverConfig.high_recall_config(),
        'diverse': NexusRetrieverConfig.diverse_results_config(),
    }
    
    config = config_map.get(config_name, NexusRetrieverConfig.default_config())
    
    # Override with kwargs
    config.update(kwargs)
    
    # Create retriever
    from ..rag.retrieval import create_retriever
    return create_retriever(vector_store, **config)
