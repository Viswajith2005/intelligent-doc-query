# BULLETPROOF FIX - Direct HTTP requests to eliminate all openai library issues
# Deployment ID: cc8bc25-bulletproof-http-only

import time
import threading
import webbrowser
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from app.utils.helpers import FileManager, ResponseFormatter
from app.services.document_loader import load_document
from app.services.chunker import chunk_document
from app.services.embedder import embed_chunks
from app.services.vector_store import store_embeddings, search_similar_chunks
from app.services.llm_service import query_llm
from app.services.evaluator import evaluate_response, evaluate_accuracy
import os
import sys
import requests
import json
from typing import List, Optional
from pydantic import BaseModel

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Document Query API",
    description="AI-powered document querying system using Azure OpenAI",
    version="1.0.0"
)

# Initialize security and file manager
security = HTTPBearer()
file_manager = FileManager()

# Get team token from environment variable
TEAM_TOKEN = os.getenv("TEAM_TOKEN", "acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a")

# Pydantic models
class DocumentQueryRequest(BaseModel):
    documents: str  # URL to the document
    questions: List[str]

class DocumentQueryResponse(BaseModel):
    answers: List[str]

# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != TEAM_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

@app.get("/")
def home():
    """Home page with basic information."""
    return HTMLResponse("""
    <html>
        <head><title>Intelligent Document Query API</title></head>
        <body>
            <h1>🤖 Intelligent Document Query API</h1>
            <p>Welcome to the AI-powered document querying system!</p>
            <p><strong>Status:</strong> ✅ Running</p>
            <p><strong>Version:</strong> 1.0.0</p>
            <p><strong>API Documentation:</strong> <a href="/docs">/docs</a></p>
            <p><strong>Health Check:</strong> <a href="/api/v1/health">/api/v1/health</a></p>
        </body>
    </html>
    """)

@app.get("/api/v1/health")
def health_check():
    """Health check endpoint."""
    # Check for critical environment variables
    required_vars = [
        "AZURE_OPENAI_CHAT_API_KEY",
        "AZURE_OPENAI_CHAT_ENDPOINT", 
        "AZURE_OPENAI_EMBEDDING_API_KEY",
        "AZURE_OPENAI_EMBEDDING_ENDPOINT"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        return {
            "status": "unhealthy",
            "message": f"Missing environment variables: {', '.join(missing_vars)}",
            "timestamp": time.time()
        }
    
    return {
        "status": "healthy",
        "message": "All systems operational",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/api/v1/test")
def test_deployment():
    """Test endpoint to verify current deployment."""
    return {
        "message": "Current deployment test",
        "timestamp": time.time(),
        "deployment_id": "latest",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.post("/api/v1/hackrx/run", response_model=DocumentQueryResponse)
async def run_document_queries(
    request: DocumentQueryRequest,
    token: str = Depends(verify_token)
):
    """
    Main endpoint to query documents with questions.
    """
    start_time = time.time()
    performance_metrics = {}
    
    try:
        print(f"📥 Downloading document from: {request.documents}")
        
        # Download document with timeout
        download_start = time.time()
        response = requests.get(request.documents, timeout=30)
        response.raise_for_status()
        document_content = response.content
        download_time = round(time.time() - download_start, 2)
        performance_metrics["download_time"] = download_time
        print(f"⏱️ Download completed in {download_time}s")
        
        # Save document
        save_start = time.time()
        filename = f"document_{int(time.time())}.pdf"
        saved_path = await file_manager.save_uploaded_file(document_content, filename)
        save_time = round(time.time() - save_start, 2)
        performance_metrics["save_time"] = save_time
        print(f"📄 Document saved in {save_time}s")
        
        # Process document
        process_start = time.time()
        text = load_document(saved_path)
        chunks = chunk_document(text)
        embeddings = embed_chunks(chunks)
        
        doc_id = file_manager.generate_document_id(filename)
        store_embeddings(doc_id, chunks, embeddings)
        process_time = round(time.time() - process_start, 2)
        performance_metrics["processing_time"] = process_time
        print(f"🔍 Document processed in {process_time}s")
        
        print(f"🔍 Processing {len(request.questions)} questions...")
        
        # Process each question
        answers = []
        question_times = []
        for i, question in enumerate(request.questions):
            try:
                question_start = time.time()
                print(f"❓ Processing question {i+1}: {question[:50]}...")
                
                # Find relevant chunks
                search_start = time.time()
                relevant_chunks = search_similar_chunks(question, doc_id, top_k=5)
                search_time = round(time.time() - search_start, 2)
                
                # Generate answer using LLM
                llm_start = time.time()
                answer = query_llm(question, relevant_chunks)
                llm_time = round(time.time() - llm_start, 2)
                
                # Clean and format the answer
                answer = answer.strip()
                if answer.startswith("Based on the document"):
                    answer = answer.replace("Based on the document, ", "").replace("Based on the document,", "")
                
                # Evaluate accuracy
                accuracy_metrics = evaluate_accuracy(question, answer)
                
                answers.append(answer)
                question_time = round(time.time() - question_start, 2)
                question_times.append(question_time)
                print(f"✅ Question {i+1} processed in {question_time}s (search: {search_time}s, LLM: {llm_time}s, accuracy: {accuracy_metrics['accuracy_score']}%)")
                
            except Exception as e:
                print(f"❌ Error processing question {i+1}: {str(e)}")
                answers.append(f"Error processing question: {str(e)}")
                question_times.append(0)
        
        elapsed = round(time.time() - start_time, 2)
        performance_metrics["total_time"] = elapsed
        performance_metrics["avg_question_time"] = round(sum(question_times) / len(question_times), 2)
        performance_metrics["question_times"] = question_times
        
        print(f"⏱️ Total processing time: {elapsed} seconds")
        print(f"📊 Performance metrics: {performance_metrics}")
        
        # Cleanup
        await file_manager.cleanup_file(saved_path)
        
        return DocumentQueryResponse(answers=answers)
        
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download document: {str(e)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Legacy endpoint for backward compatibility
@app.post("/query/")
async def query_document(file: UploadFile = File(...), query: str = ""):
    """
    Legacy endpoint to query a document (for testing purposes).
    """
    start_time = time.time()
    content = await file.read()
    saved_path = await file_manager.save_uploaded_file(content, file.filename)

    try:
        text = load_document(saved_path)
        chunks = chunk_document(text)
        embeddings = embed_chunks(chunks)

        doc_id = file_manager.generate_document_id(file.filename)
        store_embeddings(doc_id, chunks, embeddings)

        relevant_chunks = search_similar_chunks(query, doc_id)

        try:
            answer = query_llm(query, relevant_chunks)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

        await file_manager.cleanup_file(saved_path)

        return {
            "answer": answer,
            "processing_time": round(time.time() - start_time, 2)
        }

    except Exception as e:
        await file_manager.cleanup_file(saved_path)
        raise HTTPException(status_code=500, detail=str(e))

# Development-only: Auto-open browser
if os.getenv("ENVIRONMENT", "development") == "development":
    try:
        webbrowser.open_new("http://localhost:8000/docs")
    except:
        pass
