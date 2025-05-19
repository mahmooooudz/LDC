import logging
import os
import re

logger = logging.getLogger(__name__)

class Document:
    """Simple document class to store page content and metadata."""
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

class DocumentProcessor:
    def __init__(self, document_paths):
        """
        Initialize the document processor with paths to the documents.
        
        Args:
            document_paths: List of file paths to the documents
        """
        self.document_paths = document_paths
        
    def load_documents(self):
        """
        Load documents from the given file paths.
        
        Returns:
            List of Document objects
        """
        documents = []
        
        for path in self.document_paths:
            try:
                logger.info(f"Loading document: {path}")
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    documents.append(Document(
                        page_content=content,
                        metadata={"source": path}
                    ))
            except Exception as e:
                logger.error(f"Error loading document {path}: {str(e)}")
                raise
                
        return documents
    
    def process_documents(self):
        """
        Process the documents by loading and splitting them into chunks.
        
        Returns:
            List of processed document chunks
        """
        documents = self.load_documents()
        
        if not documents:
            logger.warning("No documents loaded")
            return []
            
        try:
            logger.info("Splitting documents into chunks")
            chunks = self._split_documents(documents)
            logger.info(f"Created {len(chunks)} document chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            raise
    
    def _split_documents(self, documents):
        """
        Split documents into smaller chunks based on sections.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of Document chunks
        """
        chunks = []
        
        for doc in documents:
            # Split by sections (e.g., "1. Introduction", "2. Workplace Conduct")
            sections = re.split(r'(\d+\.\s+[A-Za-z\s]+)', doc.page_content)
            
            current_section = ""
            current_title = ""
            
            for i, section in enumerate(sections):
                # If this is a section title
                if re.match(r'^\d+\.\s+[A-Za-z\s]+$', section.strip()):
                    # If we have accumulated content, save it as a chunk
                    if current_section:
                        chunks.append(Document(
                            page_content=current_title + current_section,
                            metadata={
                                "source": doc.metadata["source"],
                                "section": current_title.strip()
                            }
                        ))
                    
                    # Start a new section
                    current_title = section
                    current_section = ""
                else:
                    # This is section content
                    current_section += section
            
            # Add the last section
            if current_section:
                chunks.append(Document(
                    page_content=current_title + current_section,
                    metadata={
                        "source": doc.metadata["source"],
                        "section": current_title.strip()
                    }
                ))
            
            # Now process subsections
            new_chunks = []
            for chunk in chunks:
                # If this is a main section (not a subsection already)
                if "subsection" not in chunk.metadata:
                    # Split by subsections (e.g. "1.1 Purpose", "2.1 Code of Conduct")
                    subsections = re.split(r'(\d+\.\d+\s+[A-Za-z\s]+)', chunk.page_content)
                    
                    # If there are actual subsections (more than just the content)
                    if len(subsections) > 1:
                        current_subsection = ""
                        current_subtitle = ""
                        
                        for i, subsection in enumerate(subsections):
                            # If this is a subsection title
                            if re.match(r'^\d+\.\d+\s+[A-Za-z\s]+$', subsection.strip()):
                                # If we have accumulated content, save it as a chunk
                                if current_subsection:
                                    new_chunks.append(Document(
                                        page_content=current_subtitle + current_subsection,
                                        metadata={
                                            "source": chunk.metadata["source"],
                                            "section": chunk.metadata["section"],
                                            "subsection": current_subtitle.strip()
                                        }
                                    ))
                                
                                # Start a new subsection
                                current_subtitle = subsection
                                current_subsection = ""
                            else:
                                # This is subsection content
                                current_subsection += subsection
                        
                        # Add the last subsection
                        if current_subsection:
                            new_chunks.append(Document(
                                page_content=current_subtitle + current_subsection,
                                metadata={
                                    "source": chunk.metadata["source"],
                                    "section": chunk.metadata["section"],
                                    "subsection": current_subtitle.strip()
                                }
                            ))
                    else:
                        # No subsections, keep the original chunk
                        new_chunks.append(chunk)
                else:
                    # This is already a subsection, keep it
                    new_chunks.append(chunk)
            
            # Replace the original chunks with the new ones that include subsections
            chunks = new_chunks
        
        return chunks