from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import uuid
from datetime import datetime
import json

app = FastAPI(title="RAG Chatbot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.43:3000",  # Your local network IP
        "*"  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage directories
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# In-memory storage for job status and chat history
job_status = {}
chat_sessions = {}

# Models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[dict]
    session_id: str

class UploadStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    message: str
    files_processed: int
    total_files: int

# Import processing modules (to be created)
from document_processor import DocumentProcessor
from rag_engine import RAGEngine

# Initialize processors
doc_processor = DocumentProcessor()
rag_engine = RAGEngine()

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}

@app.post("/upload-files")
async def upload_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    """
    Handle multiple PDF file uploads
    """
    # Validate files
    if len(files) > 15:
        raise HTTPException(status_code=400, detail="Maximum 15 files allowed")
    
    job_id = str(uuid.uuid4())
    file_paths = []
    
    # Save files locally
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail=f"Only PDF files allowed: {file.filename}")
        
        # Check file size (10MB limit)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File too large: {file.filename}")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(content)
        
        file_paths.append({
            "filename": file.filename,
            "path": file_path,
            "size": len(content),
            "upload_time": datetime.now().isoformat()
        })
    
    # Initialize job status
    job_status[job_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Files uploaded, processing started",
        "files_processed": 0,
        "total_files": len(files),
        "files": file_paths
    }
    
    # Process documents in background
    background_tasks.add_task(process_documents_task, job_id, file_paths)
    
    return {"job_id": job_id, "message": "Files uploaded successfully", "total_files": len(files)}

async def process_documents_task(job_id: str, file_paths: List[dict]):
    """
    Background task to process documents
    """
    try:
        job_status[job_id]["status"] = "processing"
        job_status[job_id]["message"] = "Extracting text from PDFs"
        
        all_chunks = []
        
        for idx, file_info in enumerate(file_paths):
            job_status[job_id]["progress"] = int((idx / len(file_paths)) * 50)
            job_status[job_id]["message"] = f"Processing {file_info['filename']}"
            
            # Extract text and create chunks
            chunks = doc_processor.process_pdf(file_info['path'], file_info['filename'])
            all_chunks.extend(chunks)
            
            job_status[job_id]["files_processed"] = idx + 1
        
        # Generate embeddings and store in Pinecone
        job_status[job_id]["progress"] = 60
        job_status[job_id]["message"] = "Generating embeddings"
        
        await rag_engine.store_embeddings(all_chunks, job_id)
        
        # Save metadata
        metadata_path = os.path.join(PROCESSED_DIR, f"{job_id}_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump({
                "job_id": job_id,
                "files": file_paths,
                "chunks_count": len(all_chunks),
                "processed_at": datetime.now().isoformat()
            }, f)
        
        job_status[job_id]["status"] = "completed"
        job_status[job_id]["progress"] = 100
        job_status[job_id]["message"] = "Processing completed successfully"
        
    except Exception as e:
        job_status[job_id]["status"] = "failed"
        job_status[job_id]["message"] = f"Error: {str(e)}"

@app.get("/upload-status/{job_id}")
async def get_upload_status(job_id: str):
    """
    Get processing status for a job
    """
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_status[job_id]

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """
    Handle chat messages and return responses
    """
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Initialize session if new
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # Get chat history
    history = chat_sessions[session_id]
    
    try:
        # Get response from RAG engine
        response, sources = await rag_engine.get_response(
            query=chat_message.message,
            history=history
        )
        
        # Update chat history
        chat_sessions[session_id].append({
            "role": "user",
            "content": chat_message.message,
            "timestamp": datetime.now().isoformat()
        })
        chat_sessions[session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return ChatResponse(
            response=response,
            sources=sources,
            session_id=session_id
        )
        
    except Exception as e:
        import traceback
        print(f"ERROR in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """
    Retrieve conversation history
    """
    if session_id not in chat_sessions:
        return {"session_id": session_id, "history": []}
    
    return {"session_id": session_id, "history": chat_sessions[session_id]}

@app.delete("/chat/clear/{session_id}")
async def clear_chat(session_id: str):
    """
    Clear conversation context
    """
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    
    return {"message": "Chat history cleared", "session_id": session_id}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "pinecone_connected": rag_engine.is_connected(),
        "active_jobs": len(job_status),
        "active_sessions": len(chat_sessions)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
