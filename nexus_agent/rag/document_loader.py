"""
Document loader module for Nexus Agent RAG system.

Supports loading documents from multiple formats including PDF, Markdown,
Text, and HTML files. Extensible for additional formats.
"""

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
)
from langchain_core.documents import Document
from typing import List, Union, Dict, Any
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class NexusDocumentLoader:
    """
    Multi-format document loader for Nexus knowledge base.
    
    Supports PDF, Markdown, Text, and HTML documents with automatic
    format detection and metadata enrichment.
    """
    
    def __init__(self, data_dir: str = "nexus_agent/data/documents"):
        """
        Initialize the document loader.
        
        Args:
            data_dir: Directory path containing documents to load
        """
        self.data_dir = Path(data_dir)
        self.supported_formats = {
            '.pdf': self._load_pdf,
            '.md': self._load_text,
            '.txt': self._load_text,
            '.html': self._load_html,
            '.htm': self._load_html,
        }
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Document loader initialized with data directory: {self.data_dir}")
    
    def load_documents(
        self,
        file_paths: Union[str, List[str]] = None,
        recursive: bool = True
    ) -> List[Document]:
        """
        Load documents from specified file paths or all documents in data directory.
        
        Args:
            file_paths: Specific file paths or None to load all documents
            recursive: Whether to recursively search subdirectories
            
        Returns:
            List of loaded Document objects with metadata
        """
        if file_paths is None:
            file_paths = self._get_all_document_paths(recursive=recursive)
        elif isinstance(file_paths, str):
            file_paths = [file_paths]
        
        if not file_paths:
            logger.warning("No documents found to load")
            return []
        
        logger.info(f"Loading {len(file_paths)} document(s)...")
        all_docs = []
        
        for file_path in file_paths:
            try:
                docs = self._load_single_document(file_path)
                all_docs.extend(docs)
                logger.debug(f"Loaded {len(docs)} chunk(s) from {file_path}")
            except Exception as e:
                logger.error(f"Failed to load document {file_path}: {e}")
        
        logger.info(f"Successfully loaded {len(all_docs)} document chunks from {len(file_paths)} file(s)")
        return all_docs
    
    def _get_all_document_paths(self, recursive: bool = True) -> List[str]:
        """
        Get all supported document paths in data directory.
        
        Args:
            recursive: Whether to recursively search subdirectories
            
        Returns:
            List of file paths as strings
        """
        paths = []
        pattern = "**/*" if recursive else "*"
        
        for file_path in self.data_dir.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                paths.append(str(file_path))
        
        return sorted(paths)
    
    def _load_single_document(self, file_path: str) -> List[Document]:
        """
        Load a single document based on its file extension.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects with enriched metadata
        """
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # Load documents using appropriate loader
        loader_func = self.supported_formats[ext]
        docs = loader_func(file_path)
        
        # Enrich metadata for each document chunk
        for doc in docs:
            doc.metadata['source'] = file_path
            doc.metadata['file_type'] = ext
            doc.metadata['file_name'] = path.name
            doc.metadata['file_size'] = path.stat().st_size if path.exists() else 0
            
            # Add relative path for easier reference
            try:
                doc.metadata['relative_path'] = str(path.relative_to(self.data_dir))
            except ValueError:
                doc.metadata['relative_path'] = file_path
        
        return docs
    
    def _load_pdf(self, file_path: str) -> List[Document]:
        """
        Load PDF document using PyPDFLoader.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of Document objects (one per page)
        """
        logger.debug(f"Loading PDF: {file_path}")
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    def _load_text(self, file_path: str) -> List[Document]:
        """
        Load text or markdown document using TextLoader.
        
        Args:
            file_path: Path to text/markdown file
            
        Returns:
            List of Document objects
        """
        logger.debug(f"Loading text file: {file_path}")
        loader = TextLoader(file_path, encoding='utf-8', autodetect_encoding=True)
        return loader.load()
    
    def _load_html(self, file_path: str) -> List[Document]:
        """
        Load HTML document using WebBaseLoader.
        
        Args:
            file_path: Path to HTML file
            
        Returns:
            List of Document objects
        """
        logger.debug(f"Loading HTML file: {file_path}")
        loader = WebBaseLoader(web_paths=(f"file://{file_path}",))
        return loader.load()
    
    def get_document_stats(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Get statistics about loaded documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Dictionary with document statistics
        """
        if not documents:
            return {
                'total_documents': 0,
                'total_pages': 0,
                'total_characters': 0,
                'file_types': {},
                'files': {}
            }
        
        # Count by file type
        file_types = {}
        files = {}
        
        for doc in documents:
            file_type = doc.metadata.get('file_type', 'unknown')
            file_name = doc.metadata.get('file_name', 'unknown')
            
            file_types[file_type] = file_types.get(file_type, 0) + 1
            files[file_name] = files.get(file_name, 0) + 1
        
        total_chars = sum(len(doc.page_content) for doc in documents)
        
        return {
            'total_documents': len(documents),
            'total_pages': len(documents),
            'total_characters': total_chars,
            'average_length': total_chars / len(documents) if documents else 0,
            'file_types': file_types,
            'files': files,
        }
