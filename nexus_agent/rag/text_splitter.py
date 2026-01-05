"""
Text splitter module for Nexus Agent RAG system.

Provides multiple strategies for splitting documents into chunks,
including recursive character splitting and markdown-aware splitting.
"""

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
)
from langchain_core.documents import Document
from typing import List, Literal, Dict, Any
import logging

logger = logging.getLogger(__name__)


class NexusTextSplitter:
    """
    Text splitter with multiple strategies for different document types.
    
    Handles code blocks, tables, and structured content intelligently.
    Supports both recursive character splitting and markdown-aware splitting.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        strategy: Literal["recursive", "markdown"] = "recursive",
        add_start_index: bool = True,
    ):
        """
        Initialize the text splitter.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
            strategy: Splitting strategy ('recursive' or 'markdown')
            add_start_index: Whether to add start index to metadata
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy
        self.add_start_index = add_start_index
        
        # Initialize the default splitter based on strategy
        if strategy == "recursive":
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                add_start_index=add_start_index,
                separators=[
                    "\n\n\n",  # Multiple newlines (paragraphs)
                    "\n\n",    # Double newlines
                    "\n",      # Single newlines
                    " ",       # Spaces
                    "",        # Character level
                ]
            )
        elif strategy == "markdown":
            self.splitter = MarkdownTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                add_start_index=add_start_index,
            )
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        logger.info(
            f"Text splitter initialized: strategy={strategy}, "
            f"chunk_size={chunk_size}, chunk_overlap={chunk_overlap}"
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks based on configured strategy.
        
        Automatically selects appropriate splitter based on file type:
        - Markdown files use MarkdownTextSplitter
        - Other files use the configured strategy
        
        Args:
            documents: List of Document objects to split
            
        Returns:
            List of split Document objects
        """
        if not documents:
            logger.warning("No documents to split")
            return []
        
        logger.info(f"Splitting {len(documents)} document(s)...")
        all_splits = []
        
        for doc in documents:
            # Use appropriate splitter based on file type
            file_type = doc.metadata.get('file_type', '')
            
            if file_type in ['.md', '.markdown']:
                # Use markdown-aware splitter for markdown files
                md_splitter = MarkdownTextSplitter(
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap,
                    add_start_index=self.add_start_index,
                )
                splits = md_splitter.split_documents([doc])
                logger.debug(f"Split markdown document into {len(splits)} chunks")
            else:
                # Use configured splitter for other files
                splits = self.splitter.split_documents([doc])
                logger.debug(f"Split document into {len(splits)} chunks")
            
            all_splits.extend(splits)
        
        logger.info(f"Created {len(all_splits)} chunks from {len(documents)} document(s)")
        return all_splits
    
    def split_text(self, text: str) -> List[str]:
        """
        Split a single text string into chunks.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        return self.splitter.split_text(text)
    
    def get_split_stats(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Get statistics about document splitting.
        
        Args:
            documents: Original documents before splitting
            
        Returns:
            Dictionary with splitting statistics
        """
        if not documents:
            return {
                'total_documents': 0,
                'total_chunks': 0,
                'total_characters': 0,
                'average_chunk_size': 0,
                'chunk_size_range': (0, 0),
            }
        
        splits = self.split_documents(documents)
        
        if not splits:
            return {
                'total_documents': len(documents),
                'total_chunks': 0,
                'total_characters': 0,
                'average_chunk_size': 0,
                'chunk_size_range': (0, 0),
            }
        
        total_chars = sum(len(doc.page_content) for doc in splits)
        avg_chunk_size = total_chars / len(splits) if splits else 0
        chunk_sizes = [len(doc.page_content) for doc in splits]
        
        return {
            'total_documents': len(documents),
            'total_chunks': len(splits),
            'total_characters': total_chars,
            'average_chunk_size': avg_chunk_size,
            'chunk_size_range': (
                min(chunk_sizes) if chunk_sizes else 0,
                max(chunk_sizes) if chunk_sizes else 0
            ),
            'chunks_per_document': len(splits) / len(documents) if documents else 0,
        }
    
    def create_custom_splitter(
        self,
        separators: List[str] = None,
        keep_separator: bool = False,
        strip_whitespace: bool = True,
    ) -> RecursiveCharacterTextSplitter:
        """
        Create a custom recursive character splitter with specified separators.
        
        Args:
            separators: List of separator strings to try in order
            keep_separator: Whether to keep the separator in the chunks
            strip_whitespace: Whether to strip whitespace from chunks
            
        Returns:
            Configured RecursiveCharacterTextSplitter instance
        """
        if separators is None:
            separators = ["\n\n", "\n", " ", ""]
        
        return RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=separators,
            keep_separator=keep_separator,
            strip_whitespace=strip_whitespace,
            add_start_index=self.add_start_index,
        )
    
    def split_with_metadata_filter(
        self,
        documents: List[Document],
        metadata_filter: Dict[str, Any] = None
    ) -> List[Document]:
        """
        Split documents and filter by metadata after splitting.
        
        Args:
            documents: List of Document objects to split
            metadata_filter: Metadata key-value pairs to filter by
            
        Returns:
            List of filtered and split Document objects
        """
        splits = self.split_documents(documents)
        
        if metadata_filter:
            filtered = [
                doc for doc in splits
                if all(
                    doc.metadata.get(key) == value
                    for key, value in metadata_filter.items()
                )
            ]
            logger.info(f"Filtered to {len(filtered)} chunks from {len(splits)} total")
            return filtered
        
        return splits
