import time
import threading
import webbrowser
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

app = FastAPI(
    title="Intelligent Document Query API",
    version="1.0.0",
    description="LLM-Powered Intelligent Query–Retrieval System for insurance, legal, HR, and compliance domains"
)

file_manager = FileManager()

# Authentication
security = HTTPBearer()
TEAM_TOKEN = os.getenv("TEAM_TOKEN", "acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a")

# Pydantic models for request/response
class DocumentQueryRequest(BaseModel):
    documents: str  # URL to the document
    questions: List[str]

class DocumentQueryResponse(BaseModel):
    answers: List[str]

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the Bearer token"""
    if credentials.credentials != TEAM_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

@app.get("/")
def home():
    """
    Root endpoint: shows a welcome message.
    """
    return {"message": "Welcome to Intelligent Document Query API! Visit /docs to try the API."}

@app.get("/api/v1/health")
def health_check():
    """
    Health check endpoint for the API.
    """
    # Check if required environment variables are set
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
            "error": "Configuration incomplete"
        }
    
    return {"status": "healthy", "message": "API is running successfully"}

@app.post("/api/v1/hackrx/run", response_model=DocumentQueryResponse)
async def run_document_queries(
    request: DocumentQueryRequest,
    token: str = Depends(verify_token)
):
    """
    Main endpoint to process document queries according to hackathon specifications.
    
    This endpoint:
    1. Downloads document from the provided URL
    2. Processes each question using the intelligent query system
    3. Returns structured answers in the required format
    """
    start_time = time.time()
    performance_metrics = {}
    
    try:
        # Download document from URL
        download_start = time.time()
        print(f"📥 Downloading document from: {request.documents}")
        response = requests.get(request.documents, timeout=30)
        response.raise_for_status()
        download_time = round(time.time() - download_start, 2)
        performance_metrics["download_time"] = download_time
        print(f"⏱️ Download completed in {download_time}s")
        
        # Save the downloaded document
        save_start = time.time()
        document_content = response.content
        filename = "policy_document.pdf"
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

        evaluation = evaluate_response(query, answer)

        elapsed = round(time.time() - start_time, 2)

        return ResponseFormatter.format_success_response({
            "query": query,
            "answer": answer,
            "evaluation": evaluation,
            "execution_time_seconds": elapsed
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    finally:
        await file_manager.cleanup_file(saved_path)

# Only auto-open browser in development
if __name__ == "__main__":
    # Check if running in development mode
    if os.getenv("ENVIRONMENT", "development") == "development":
        # Open browser after 1.5 sec delay
        threading.Timer(1.5, lambda: webbrowser.open_new("http://127.0.0.1:8000/docs")).start()

    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
