"""
RAG (Retrieval-Augmented Generation) module for Nexus Agent.

This module provides document loading, text splitting, embedding generation,
vector storage, and retrieval capabilities for knowledge-based responses.
"""

from .document_loader import NexusDocumentLoader
from .text_splitter import NexusTextSplitter
from .embeddings import NexusEmbeddings
from .vector_store import NexusVectorStore
from .indexing import NexusIndexingPipeline
from .retrieval import NexusRetriever

__all__ = [
    "NexusDocumentLoader",
    "NexusTextSplitter",
    "NexusEmbeddings",
    "NexusVectorStore",
    "NexusIndexingPipeline",
    "NexusRetriever",
]
