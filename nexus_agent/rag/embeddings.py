"""
Embeddings module for Nexus Agent RAG system.

Provides embedding generation using BGE (BAAI) models optimized for
Chinese text understanding and semantic search.
"""

from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class NexusEmbeddings:
    """
    Embedding model wrapper using BGE (BAAI) Chinese embeddings.
    
    Optimized for Chinese text understanding and semantic search.
    Uses sentence-transformers backend with HuggingFace integration.
    """
    
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-zh-v1.5",
        device: str = "cpu",
        normalize_embeddings: bool = True,
        encode_kwargs: Optional[dict] = None,
    ):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the BGE model to use
            device: Device to run model on ('cpu' or 'cuda')
            normalize_embeddings: Whether to normalize embeddings (important for BGE)
            encode_kwargs: Additional encoding arguments
        """
        self.model_name = model_name
        self.device = device
        self.normalize_embeddings = normalize_embeddings
        
        # Default encode kwargs for BGE models
        default_encode_kwargs = {
            'normalize_embeddings': normalize_embeddings,
            'batch_size': 32,
        }
        
        if encode_kwargs:
            default_encode_kwargs.update(encode_kwargs)
        
        self.encode_kwargs = default_encode_kwargs
        
        # Initialize sentence-transformers model
        logger.info(f"Initializing embeddings model: {model_name}")
        logger.info(f"Device: {device}, Normalize embeddings: {normalize_embeddings}")
        
        # SentenceTransformer expects model name as first positional argument
        # Note: normalize_embeddings is handled in encode() method, not __init__()
        self.model = SentenceTransformer(
            model_name,  # Positional argument
            device=device
        )
        
        logger.info("Embeddings model initialized successfully")
    
    def get_embeddings_model(self) -> Embeddings:
        """
        Get a LangChain-compatible embeddings wrapper.
        
        Returns:
            LangChain Embeddings instance wrapping the sentence-transformers model
        """
        return HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={'device': self.device},
            encode_kwargs=self.encode_kwargs,
        )
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.
        
        Args:
            text: Query text to embed (supports Chinese)
            
        Returns:
            List of float values representing the embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple document texts.
        
        Args:
            texts: List of document texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            Dimension of the embedding vectors
        """
        # Get dimension from model
        return self.model.get_sentence_embedding_dimension()
    
    def compute_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        import numpy as np
        
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def batch_embed(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = False,
    ) -> List[List[float]]:
        """
        Embed texts in batches for better performance.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch
            show_progress: Whether to show progress bar
            
        Returns:
            List of embedding vectors
        """
        logger.info(f"Embedding {len(texts)} texts in batches of {batch_size}")
        
        # Update encode kwargs for this batch
        original_kwargs = self.encode_kwargs.copy()
        self.encode_kwargs['batch_size'] = batch_size
        self.encode_kwargs['show_progress_bar'] = show_progress
        
        try:
            embeddings = self.embed_documents(texts)
            logger.info(f"Successfully embedded {len(embeddings)} texts")
            return embeddings
        finally:
            # Restore original kwargs
            self.encode_kwargs = original_kwargs


class EmbeddingCache:
    """
    Simple in-memory cache for embeddings to avoid recomputation.
    """
    
    def __init__(self, max_size: int = 10000):
        """
        Initialize the embedding cache.
        
        Args:
            max_size: Maximum number of embeddings to cache
        """
        self.cache: dict[str, List[float]] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, text: str) -> Optional[List[float]]:
        """
        Get cached embedding for a text.
        
        Args:
            text: Text to look up
            
        Returns:
            Cached embedding or None if not found
        """
        embedding = self.cache.get(text)
        if embedding is not None:
            self.hits += 1
        else:
            self.misses += 1
        return embedding
    
    def set(self, text: str, embedding: List[float]) -> None:
        """
        Cache an embedding for a text.
        
        Args:
            text: Text to cache
            embedding: Embedding vector to cache
        """
        # Evict oldest entry if cache is full
        if len(self.cache) >= self.max_size:
            # Simple FIFO eviction
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[text] = embedding
    
    def clear(self) -> None:
        """Clear all cached embeddings."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Embedding cache cleared")
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
        }
