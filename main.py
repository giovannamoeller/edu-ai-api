from fastapi import FastAPI, HTTPException
from models import EssayRequest, EssayResponse
from services import EssayAnalysisService
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="ENEM Essay Analysis API",
    description="API for analyzing ENEM essays using AI",
    version="1.0.0"
)

# Initialize the essay analysis service
essay_service = EssayAnalysisService(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name=os.getenv("MODEL_NAME", "gpt-4")
)

@app.post("/analyze-essay", response_model=EssayResponse)
async def analyze_essay(request: EssayRequest):
    print(request)
    try:
        response = await essay_service.analyze_essay(
            text=request.text,
            subject=request.subject
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Optional: Add a route to get API information
@app.get("/")
async def root():
    return {
        "name": "ENEM Essay Analysis API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }