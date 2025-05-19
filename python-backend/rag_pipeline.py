from document_processor import DocumentProcessor
import logging
import re

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, document_paths):
        """
        Initialize the RAG pipeline with paths to the documents.
        
        Args:
            document_paths: List of file paths to the documents
        """
        self.document_processor = DocumentProcessor(document_paths)
        self.setup_pipeline()
        
    def setup_pipeline(self):
        """
        Set up a simple keyword-based search pipeline.
        """
        try:
            # Process documents
            self.chunks = self.document_processor.process_documents()
            
            if not self.chunks:
                raise ValueError("No document chunks available for indexing")
            
            logger.info(f"Loaded {len(self.chunks)} document chunks for search")
            
        except Exception as e:
            logger.error(f"Error setting up pipeline: {str(e)}")
            raise
    
    def process_query(self, query):
        """
        Process a user query using keyword matching.
        
        Args:
            query: User's query string
            
        Returns:
            Response from the pipeline
        """
        try:
            logger.info(f"Processing query: {query}")
            
            # Convert query to lowercase for better matching
            query_lower = query.lower()
            
            # Extract important keywords
            keywords = self._extract_keywords(query_lower)
            
            if not keywords:
                return "I'm sorry, I couldn't understand your query. Could you please be more specific about which HR policy you're asking about?"
            
            # Find relevant chunks based on keyword matching
            relevant_chunks = []
            
            for chunk in self.chunks:
                content_lower = chunk.page_content.lower()
                score = self._calculate_relevance(content_lower, keywords)
                if score > 0:
                    # Store the chunk and its score
                    relevant_chunks.append((score, chunk))
            
            if not relevant_chunks:
                return "I couldn't find information about that in the HR policy. Could you try rephrasing your question?"
            
            # Sort chunks by score (descending)
            relevant_chunks.sort(key=lambda x: x[0], reverse=True)
            
            # Extract just the top 2 chunks
            top_chunks = [chunk for _, chunk in relevant_chunks[:2]]
            
            # Generate response based on the most relevant chunks
            return self._generate_response(query, top_chunks)
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    def _extract_keywords(self, query):
        """Extract important keywords from the query."""
        # List of common HR policy topics from the documents
        hr_topics = [
            "leave", "vacation", "sick", "maternity", "paternity", "holiday",
            "working hours", "overtime", "salary", "compensation", "bonus",
            "health insurance", "termination", "resignation", "harassment",
            "conduct", "discipline", "confidentiality", "data protection"
        ]
        
        # Extract specific keywords from query
        keywords = []
        for topic in hr_topics:
            if topic in query:
                keywords.append(topic)
        
        # If no specific topics were found, use general words minus stopwords
        if not keywords:
            stopwords = ["a", "an", "the", "is", "are", "what", "how", "can", "do", "does", 
                         "about", "me", "my", "tell", "know", "would", "could", "should", "i"]
            words = [word for word in query.split() if word not in stopwords and len(word) > 2]
            keywords = words
            
        return keywords
    
    def _calculate_relevance(self, content, keywords):
        """Calculate relevance score based on keyword matches."""
        score = 0
        for keyword in keywords:
            if keyword in content:
                # Count occurrences of the keyword
                count = content.count(keyword)
                score += count
                
                # Bonus points for section titles containing the keyword
                section_match = re.search(r'\d+\.\d+\s+.*' + keyword + '.*', content, re.IGNORECASE)
                if section_match:
                    score += 5
        
        return score
    
    def _generate_response(self, query, chunks):
        """Generate a response based on the relevant chunks."""
        if not chunks:
            return "I'm sorry, I couldn't find information related to your query in the HR policy."
        
        # Combine content from the most relevant chunks
        combined_content = "\n\n".join([chunk.page_content for chunk in chunks])
        
        # Format based on query type
        if "what" in query.lower() or "how" in query.lower() or "tell me about" in query.lower():
            return f"According to the XYZ Company HR policy:\n\n{combined_content}"
        
        elif "where" in query.lower():
            return f"Based on the HR policy documents:\n\n{combined_content}"
        
        elif "when" in query.lower():
            return f"The HR policy states:\n\n{combined_content}"
        
        elif "who" in query.lower():
            return f"According to XYZ Company's HR policy:\n\n{combined_content}"
        
        elif "why" in query.lower():
            return f"The company's HR policy explains:\n\n{combined_content}"
        
        else:
            return f"Here's what I found in the HR policy regarding your question:\n\n{combined_content}"