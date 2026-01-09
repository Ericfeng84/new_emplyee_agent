"""
Document Processing Demo Script for Nexus Agent.

Demonstrates the document loading, splitting, and preprocessing
capabilities of the RAG system.
"""

from nexus_agent.rag.document_loader import NexusDocumentLoader
from nexus_agent.rag.text_splitter import NexusTextSplitter
from nexus_agent.utils.data_preprocessing import DataPreprocessor


def run_document_processing_demo():
    """
    Demonstrate complete document processing pipeline.
    
    This demo shows:
    1. Document loading from multiple formats
    2. Document analysis and statistics
    3. Text splitting strategies
    4. Data preprocessing and cleaning
    5. Table and code block extraction
    """
    print("=" * 70)
    print("Nexus Document Processing Demo")
    print("=" * 70)
    print()
    
    # Step 1: Load documents
    print("Step 1: Loading documents...")
    print("-" * 70)
    
    loader = NexusDocumentLoader(data_dir="nexus_agent/data/documents")
    docs = loader.load_documents()
    
    print(f"✅ Loaded {len(docs)} document(s)")
    print()
    
    # Step 2: Analyze documents
    print("Step 2: Document analysis...")
    print("-" * 70)
    print()
    
    doc_stats = loader.get_document_stats(docs)
    
    print(f"Total documents: {doc_stats['total_documents']}")
    print(f"Total characters: {doc_stats['total_characters']:,}")
    print(f"Average length: {doc_stats['average_length']:.0f} characters")
    print()
    print("File types:")
    for file_type, count in doc_stats['file_types'].items():
        print(f"  - {file_type}: {count} document(s)")
    print()
    print("Files:")
    for file_name, count in doc_stats['files'].items():
        print(f"  - {file_name}: {count} page(s)/chunk(s)")
    print()
    
    # Show document details
    print("Document details:")
    print("-" * 70)
    for i, doc in enumerate(docs[:3], 1):  # Show first 3
        print(f"\nDocument {i}:")
        print(f"  File: {doc.metadata.get('file_name', 'Unknown')}")
        print(f"  Type: {doc.metadata.get('file_type', 'Unknown')}")
        print(f"  Length: {len(doc.page_content)} characters")
        print(f"  Preview: {doc.page_content[:150]}...")
    print()
    
    # Step 3: Split documents
    print("Step 3: Splitting documents...")
    print("-" * 70)
    print()
    
    # Test different splitting strategies
    strategies = ["recursive", "markdown"]
    
    for strategy in strategies:
        print(f"\nStrategy: {strategy}")
        print(f"{'-' * 70}")
        
        splitter = NexusTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            strategy=strategy
        )
        
        splits = splitter.split_documents(docs)
        stats = splitter.get_split_stats(docs)
        
        print(f"  Chunks created: {stats['total_chunks']}")
        print(f"  Average chunk size: {stats['average_chunk_size']:.0f} characters")
        print(f"  Chunk size range: {stats['chunk_size_range'][0]} - {stats['chunk_size_range'][1]} characters")
        print(f"  Chunks per document: {stats['chunks_per_document']:.1f}")
    
    print()
    
    # Show sample chunks
    print("\nSample chunks (using recursive strategy):")
    print("-" * 70)
    
    splitter = NexusTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        strategy="recursive"
    )
    
    splits = splitter.split_documents(docs)
    
    for i, split in enumerate(splits[:5], 1):  # Show first 5 chunks
        print(f"\nChunk {i}:")
        print(f"  Source: {split.metadata.get('file_name', 'Unknown')}")
        print(f"  Length: {len(split.page_content)} characters")
        print(f"  Content: {split.page_content[:200]}...")
    print()
    
    # Step 4: Data preprocessing
    print("Step 4: Data preprocessing...")
    print("-" * 70)
    print()
    
    # Create sample text with issues
    sample_text = """
    This  is  a  sample  text  with  extra  spaces.
    
    It also has multiple
    
    newlines.
    
    And some formatting issues like . spaced . punctuation .
    
    Visit https://example.com for more info.
    Contact us at test@example.com
    """
    
    print("Original text:")
    print(sample_text)
    print()
    
    # Clean the text
    cleaned = DataPreprocessor.clean_text(sample_text)
    print("Cleaned text:")
    print(cleaned)
    print()
    
    # Remove URLs and emails
    no_urls = DataPreprocessor.remove_urls(cleaned)
    no_emails = DataPreprocessor.remove_email_addresses(no_urls)
    
    print("After removing URLs and emails:")
    print(no_emails)
    print()
    
    # Step 5: Table extraction
    print("Step 5: Table extraction...")
    print("-" * 70)
    print()
    
    # Create sample markdown table
    sample_table = """
| 员工姓名 | 部门 | 职位 |
|---------|------|------|
| 张三 | 技术部 | 工程师 |
| 李四 | 市场部 | 经理 |
| 王五 | 人力资源部 | 专员 |
"""
    
    print("Sample markdown table:")
    print(sample_table)
    print()
    
    tables = DataPreprocessor.extract_tables(sample_table)
    print(f"Extracted {len(tables)} table(s)")
    print()
    
    if tables:
        table = tables[0]
        print("Formatted as text:")
        print(DataPreprocessor.format_table_as_text(table))
        print()
        
        print("Formatted as markdown:")
        print(DataPreprocessor.format_table_as_markdown(table))
        print()
    
    # Step 6: Code block extraction
    print("Step 6: Code block extraction...")
    print("-" * 70)
    print()
    
    # Create sample markdown with code
    sample_code = """
Here's a Python function:

```python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```

And here's some JavaScript:

```javascript
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("World"));
```
"""
    
    print("Sample markdown with code blocks:")
    print(sample_code)
    print()
    
    code_blocks = DataPreprocessor.extract_code_blocks(sample_code)
    print(f"Extracted {len(code_blocks)} code block(s)")
    print()
    
    for i, block in enumerate(code_blocks, 1):
        print(f"Code block {i}:")
        print(f"  Language: {block['language']}")
        print(f"  Code: {block['code'][:100]}...")
        print()
    
    # Step 7: Heading extraction
    print("Step 7: Heading extraction...")
    print("-" * 70)
    print()
    
    # Create sample markdown with headings
    sample_headings = """
# Main Heading

Content under main heading.

## Sub Heading 1

Content under sub heading 1.

### Sub-sub Heading

Content under sub-sub heading.

## Sub Heading 2

Content under sub heading 2.
"""
    
    print("Sample markdown with headings:")
    print(sample_headings)
    print()
    
    headings = DataPreprocessor.extract_headings(sample_headings)
    print(f"Extracted {len(headings)} heading(s)")
    print()
    
    for i, heading in enumerate(headings, 1):
        indent = "  " * (heading['level'] - 1)
        print(f"{indent}{'#' * heading['level']} {heading['content']}")
    print()
    
    # Step 8: Section splitting
    print("Step 8: Section splitting...")
    print("-" * 70)
    print()
    
    sections = DataPreprocessor.split_by_headings(sample_headings)
    print(f"Split into {len(sections)} section(s)")
    print()
    
    for i, section in enumerate(sections, 1):
        if section['heading']:
            print(f"Section {i}: {section['heading']}")
        else:
            print(f"Section {i}: (No heading)")
        print(f"  Content preview: {section['content'][:100]}...")
        print()
    
    # Step 9: Language detection
    print("Step 9: Language detection...")
    print("-" * 70)
    print()
    
    test_texts = [
        ("Chinese text", "这是一段中文文本"),
        ("English text", "This is English text"),
        ("Mixed text", "This is mixed 中英文文本"),
    ]
    
    for name, text in test_texts:
        language = DataPreprocessor.detect_language(text)
        print(f"{name}: {language}")
    print()
    
    # Step 10: Key phrase extraction
    print("Step 10: Key phrase extraction...")
    print("-" * 70)
    print()
    
    sample_phrases = """
The Human Resources Department manages employee relations and benefits.
The Information Technology Department provides technical support and infrastructure.
The Marketing Department handles advertising and brand management.
"""
    
    print("Sample text:")
    print(sample_phrases)
    print()
    
    phrases = DataPreprocessor.extract_key_phrases(sample_phrases, min_length=2)
    print(f"Extracted {len(phrases)} key phrase(s)")
    print()
    
    for i, phrase in enumerate(phrases, 1):
        print(f"  {i}. {phrase}")
    print()
    
    # Final summary
    print("=" * 70)
    print("Demo Summary")
    print("=" * 70)
    print()
    print("✅ Document loading: Supports PDF, Markdown, Text, HTML")
    print("✅ Document splitting: Recursive and markdown-aware strategies")
    print("✅ Data preprocessing: Text cleaning, URL/email removal")
    print("✅ Table extraction: Markdown table parsing and formatting")
    print("✅ Code extraction: Multi-language code block detection")
    print("✅ Heading extraction: Multi-level heading detection")
    print("✅ Section splitting: Content segmentation by headings")
    print("✅ Language detection: Chinese, English, and mixed text")
    print("✅ Key phrase extraction: Capitalized phrase detection")
    print()
    print("Demo completed successfully!")
    print()


def run_preprocessing_test():
    """
    Run preprocessing tests on sample documents.
    """
    print("=" * 70)
    print("Preprocessing Test")
    print("=" * 70)
    print()
    
    # Load documents
    loader = NexusDocumentLoader(data_dir="nexus_agent/data/documents")
    docs = loader.load_documents()
    
    print(f"Loaded {len(docs)} document(s)")
    print()
    
    # Process each document
    for i, doc in enumerate(docs, 1):
        print(f"Document {i}: {doc.metadata.get('file_name', 'Unknown')}")
        print("-" * 70)
        
        # Detect language
        language = DataPreprocessor.detect_language(doc.page_content)
        print(f"Language: {language}")
        
        # Extract headings
        headings = DataPreprocessor.extract_headings(doc.page_content)
        print(f"Headings: {len(headings)}")
        
        # Extract tables
        tables = DataPreprocessor.extract_tables(doc.page_content)
        print(f"Tables: {len(tables)}")
        
        # Extract code blocks
        code_blocks = DataPreprocessor.extract_code_blocks(doc.page_content)
        print(f"Code blocks: {len(code_blocks)}")
        
        # Extract key phrases
        phrases = DataPreprocessor.extract_key_phrases(doc.page_content)
        print(f"Key phrases: {len(phrases)}")
        
        print()
    
    print("Preprocessing test completed!")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_preprocessing_test()
    else:
        run_document_processing_demo()
