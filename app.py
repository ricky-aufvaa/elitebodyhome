from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time
import sys
import os

# Add src directory to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.graph import graph
from src.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage

# Initialize FastAPI app
app = FastAPI(
    title="Elite Body Home RAG API",
    description="Agentic RAG API for Elite Body Home Polyclinic",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    metadata: dict

class HealthResponse(BaseModel):
    status: str
    message: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API is running"""
    return HealthResponse(
        status="healthy",
        message="Elite Body Home RAG API is running"
    )

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user questions using the agentic RAG system
    """
    try:
        start_time = time.time()
        
        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Create input for the graph
        input_data = {
            "question": HumanMessage(content=request.message.strip())
        }
        
        # Use provided session_id or generate a default one
        # This allows for conversation continuity when session_id is provided
        thread_id = request.session_id if request.session_id else f"session_{int(time.time() * 1000)}"
        config = {"configurable": {"thread_id": thread_id}}
        result = graph.invoke(input=input_data, config=config)
        
        # Extract the final AI response from messages
        ai_response = "I'm sorry, I couldn't process your request."
        on_topic = False
        documents_retrieved = 0
        
        if "messages" in result and result["messages"]:
            # Get the last AI message
            for message in reversed(result["messages"]):
                if isinstance(message, AIMessage):
                    ai_response = message.content
                    break
        
        # Extract metadata from the final state
        if "on_topic" in result:
            on_topic = result["on_topic"].lower() == "yes" if result["on_topic"] else False
        
        if "documents" in result and result["documents"]:
            documents_retrieved = len(result["documents"])
        
        processing_time = round(time.time() - start_time, 2)
        
        # Prepare response
        response = ChatResponse(
            response=ai_response,
            metadata={
                "on_topic": on_topic,
                "documents_retrieved": documents_retrieved,
                "processing_time": processing_time,
                "rephrased_question": result.get("rephrased_question", ""),
                "rephrase_count": result.get("rephrase_count", 0)
            }
        )
        
        return response
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Elite Body Home RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
