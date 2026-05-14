from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Recruitment Onboarding System",
    description="AI-powered recruitment and onboarding system with WhatsApp integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verify environment variables
@app.on_event("startup")
async def startup_event():
    """Verify all required environment variables are set"""
    required_vars = [
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_PHONE_NUMBER",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
    else:
        logger.info("✅ All environment variables loaded successfully!")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "recruitment-onboarding-system",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Recruitment Onboarding System API",
        "docs": "/docs",
        "health": "/health"
    }

# WhatsApp webhook endpoint (placeholder)
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """WhatsApp webhook for receiving messages"""
    try:
        data = await request.json()
        logger.info(f"WhatsApp message received: {data}")
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid webhook data")

# AI Chat endpoint (placeholder)
@app.post("/api/chat")
async def chat(request: Request):
    """Chat endpoint for AI interactions"""
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Placeholder for OpenAI integration
        logger.info(f"Chat message received: {message}")
        
        return {
            "status": "processing",
            "message": "AI response would go here"
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error processing chat request")

# Candidates endpoint (placeholder)
@app.get("/api/candidates")
async def get_candidates():
    """Get all candidates"""
    return {
        "candidates": [],
        "total": 0
    }

@app.post("/api/candidates")
async def create_candidate(request: Request):
    """Create a new candidate"""
    try:
        data = await request.json()
        logger.info(f"New candidate created: {data}")
        return {
            "status": "created",
            "candidate": data
        }
    except Exception as e:
        logger.error(f"Error creating candidate: {e}")
        raise HTTPException(status_code=400, detail="Error creating candidate")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
