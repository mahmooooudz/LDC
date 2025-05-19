from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import RAGPipeline
import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="HR Policy Chatbot Backend")

# Initialize RAG pipeline
pipeline = None

class Query(BaseModel):
    query: str

class Response(BaseModel):
    response: str

@app.on_event("startup")
async def startup_event():
    global pipeline
    try:
        # Initialize RAG pipeline with the HR policy documents
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        document_paths = [
            os.path.join(data_dir, "HR_Policy_Dataset1.txt"),
            os.path.join(data_dir, "HR_Policy_Dataset2.txt")
        ]
        pipeline = RAGPipeline(document_paths)
        logger.info("RAG pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing RAG pipeline: {str(e)}")
        raise

@app.post("/api/chat", response_model=Response)
async def process_query(query: Query):
    if not query.query or query.query.strip() == "":
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="RAG pipeline not initialized")
    
    try:
        logger.info(f"Processing query: {query.query}")
        response = pipeline.process_query(query.query)
        return Response(response=response)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)