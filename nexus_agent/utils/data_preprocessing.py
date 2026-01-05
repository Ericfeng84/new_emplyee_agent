"""
Data preprocessing utilities for Nexus Agent RAG system.

Provides document cleaning, table extraction, and text normalization
functions to prepare documents for indexing.
"""

import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Utility class for cleaning and preprocessing document content.
    
    Handles tables, formatting issues, and noise to improve
    the quality of indexed documents.
    """
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing excessive whitespace, special characters, etc.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
        text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines to double
        
        # Remove control characters except newlines and tabs
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Fix common formatting issues
        text = text.replace(' .', '.')  # Fix spaced periods
        text = text.replace(' ,', ',')  # Fix spaced commas
        text = text.replace(' ;', ';')  # Fix spaced semicolons
        text = text.replace(' :', ':')  # Fix spaced colons
        text = text.replace('( ', '(')  # Fix spaced opening parentheses
        text = text.replace(' )', ')')  # Fix spaced closing parentheses
        
        # Remove bullet point artifacts
        text = re.sub(r'•\s*', '• ', text)  # Normalize bullets
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Text to normalize
            
        Returns:
            Text with normalized whitespace
        """
        if not text:
            return ""
        
        # Replace all whitespace sequences with single space
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """
        Remove URLs from text.
        
        Args:
            text: Text to process
            
        Returns:
            Text without URLs
        """
        # Remove HTTP/HTTPS URLs
        text = re.sub(r'https?://\S+', '', text)
        
        # Remove www URLs
        text = re.sub(r'www\.\S+', '', text)
        
        return text
    
    @staticmethod
    def remove_email_addresses(text: str) -> str:
        """
        Remove email addresses from text.
        
        Args:
            text: Text to process
            
        Returns:
            Text without email addresses
        """
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    
    @staticmethod
    def extract_tables(text: str) -> List[Dict[str, Any]]:
        """
        Extract tables from markdown text.
        
        Args:
            text: Markdown text containing tables
            
        Returns:
            List of dictionaries representing tables
        """
        tables = []
        
        # Markdown table pattern
        # | header1 | header2 | header3 |
        # |----------|----------|----------|
        # | cell1    | cell2    | cell3    |
        table_pattern = r'\|(.+)\|\n\|[-:| ]+\|\n((?:\|.+\|\n)+)'
        
        for match in re.finditer(table_pattern, text):
            # Parse header
            header_line = match.group(1).strip()
            header = [cell.strip() for cell in header_line.split('|')]
            
            # Parse rows
            rows = []
            row_lines = match.group(2).strip().split('\n')
            
            for row_line in row_lines:
                cells = [cell.strip() for cell in row_line.split('|')]
                # Filter out empty cells from leading/trailing pipes
                cells = [cell for cell in cells if cell or cells.index(cell) not in [0, len(cells)-1]]
                if cells:
                    rows.append(cells)
            
            tables.append({
                'header': header,
                'rows': rows,
                'raw_text': match.group(0)
            })
        
        logger.info(f"Extracted {len(tables)} table(s) from text")
        return tables
    
    @staticmethod
    def format_table_as_text(table: Dict[str, Any]) -> str:
        """
        Format a table dictionary as readable text.
        
        Args:
            table: Table dictionary with header and rows
            
        Returns:
            Formatted text representation of the table
        """
        lines = []
        
        # Header
        lines.append("表格:")
        lines.append(" | ".join(table['header']))
        lines.append("-" * len(" | ".join(table['header'])))
        
        # Rows
        for row in table['rows']:
            lines.append(" | ".join(row))
        
        return "\n".join(lines)
    
    @staticmethod
    def format_table_as_markdown(table: Dict[str, Any]) -> str:
        """
        Format a table dictionary as markdown.
        
        Args:
            table: Table dictionary with header and rows
            
        Returns:
            Markdown table string
        """
        lines = []
        
        # Header
        header = " | ".join(table['header'])
        lines.append(f"| {header} |")
        
        # Separator
        separator = " | ".join(["---"] * len(table['header']))
        lines.append(f"| {separator} |")
        
        # Rows
        for row in table['rows']:
            row_text = " | ".join(row)
            lines.append(f"| {row_text} |")
        
        return "\n".join(lines)
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown text.
        
        Args:
            text: Markdown text containing code blocks
            
        Returns:
            List of dictionaries representing code blocks
        """
        code_blocks = []
        
        # Code block pattern: ```language\ncode\n```
        code_pattern = r'```(\w*)\n(.*?)```'
        
        for match in re.finditer(code_pattern, text, re.DOTALL):
            language = match.group(1) or 'text'
            code = match.group(2)
            
            code_blocks.append({
                'language': language,
                'code': code,
                'raw_text': match.group(0)
            })
        
        logger.info(f"Extracted {len(code_blocks)} code block(s) from text")
        return code_blocks
    
    @staticmethod
    def remove_code_blocks(text: str) -> str:
        """
        Remove code blocks from text.
        
        Args:
            text: Text to process
            
        Returns:
            Text without code blocks
        """
        return re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    
    @staticmethod
    def extract_headings(text: str) -> List[Dict[str, str]]:
        """
        Extract headings from markdown text.
        
        Args:
            text: Markdown text containing headings
            
        Returns:
            List of dictionaries representing headings
        """
        headings = []
        
        # Heading pattern: # Heading or ## Heading, etc.
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        
        for line in text.split('\n'):
            match = re.match(heading_pattern, line.strip())
            if match:
                level = len(match.group(1))
                content = match.group(2)
                
                headings.append({
                    'level': level,
                    'content': content,
                    'raw_text': line
                })
        
        logger.info(f"Extracted {len(headings)} heading(s) from text")
        return headings
    
    @staticmethod
    def split_by_headings(text: str) -> List[Dict[str, str]]:
        """
        Split text into sections based on headings.
        
        Args:
            text: Text to split
            
        Returns:
            List of dictionaries representing sections
        """
        sections = []
        current_section = {'heading': None, 'content': []}
        
        for line in text.split('\n'):
            # Check if line is a heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            
            if heading_match:
                # Save previous section
                if current_section['heading'] or current_section['content']:
                    sections.append({
                        'heading': current_section['heading'],
                        'content': '\n'.join(current_section['content']).strip()
                    })
                
                # Start new section
                current_section = {
                    'heading': heading_match.group(2),
                    'content': []
                }
            else:
                current_section['content'].append(line)
        
        # Add last section
        if current_section['heading'] or current_section['content']:
            sections.append({
                'heading': current_section['heading'],
                'content': '\n'.join(current_section['content']).strip()
            })
        
        logger.info(f"Split text into {len(sections)} section(s)")
        return sections
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect the primary language of the text.
        
        Simple heuristic based on character ranges.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code ('zh' for Chinese, 'en' for English, 'mixed' for both)
        """
        if not text:
            return 'unknown'
        
        # Count Chinese characters
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        
        # Count English characters
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        total_chars = chinese_chars + english_chars
        
        if total_chars == 0:
            return 'unknown'
        
        chinese_ratio = chinese_chars / total_chars
        english_ratio = english_chars / total_chars
        
        if chinese_ratio > 0.7:
            return 'zh'
        elif english_ratio > 0.7:
            return 'en'
        else:
            return 'mixed'
    
    @staticmethod
    def preprocess_document(
        text: str,
        clean: bool = True,
        remove_urls: bool = False,
        remove_emails: bool = False,
        normalize: bool = False,
    ) -> str:
        """
        Apply multiple preprocessing steps to a document.
        
        Args:
            text: Text to preprocess
            clean: Whether to clean text
            remove_urls: Whether to remove URLs
            remove_emails: Whether to remove email addresses
            normalize: Whether to normalize whitespace
            
        Returns:
            Preprocessed text
        """
        result = text
        
        if clean:
            result = DataPreprocessor.clean_text(result)
        
        if remove_urls:
            result = DataPreprocessor.remove_urls(result)
        
        if remove_emails:
            result = DataPreprocessor.remove_email_addresses(result)
        
        if normalize:
            result = DataPreprocessor.normalize_whitespace(result)
        
        return result
    
    @staticmethod
    def extract_key_phrases(text: str, min_length: int = 3) -> List[str]:
        """
        Extract key phrases from text.
        
        Simple heuristic based on capitalized words and common patterns.
        
        Args:
            text: Text to analyze
            min_length: Minimum phrase length in words
            
        Returns:
            List of key phrases
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        phrases = []
        
        for sentence in sentences:
            # Extract capitalized phrases
            # Pattern: Capitalized word followed by more capitalized words
            capitalized_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
            
            for match in re.finditer(capitalized_pattern, sentence):
                phrase = match.group(0)
                words = phrase.split()
                
                if len(words) >= min_length:
                    phrases.append(phrase)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_phrases = []
        
        for phrase in phrases:
            if phrase.lower() not in seen:
                seen.add(phrase.lower())
                unique_phrases.append(phrase)
        
        logger.info(f"Extracted {len(unique_phrases)} key phrase(s)")
        return unique_phrases


def batch_preprocess(
    texts: List[str],
    clean: bool = True,
    normalize: bool = False,
) -> List[str]:
    """
    Preprocess a batch of texts.
    
    Args:
        texts: List of texts to preprocess
        clean: Whether to clean text
        normalize: Whether to normalize whitespace
        
    Returns:
        List of preprocessed texts
    """
    logger.info(f"Batch preprocessing {len(texts)} text(s)")
    
    results = []
    for text in texts:
        result = DataPreprocessor.preprocess_document(
            text,
            clean=clean,
            normalize=normalize
        )
        results.append(result)
    
    return results
