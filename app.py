from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from impact_analyzer.analyzer import analyze_change_request
from pydantic import BaseModel
from typing import Any, Dict
import os
import logging
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # ✅ Fixed typo from GENIMI to GEMINI

if not GEMINI_API_KEY:
    logging.warning("⚠️ GEMINI_API_KEY is not set. Check your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChangeRequest(BaseModel):
    change_text: str

# API endpoint
@app.post("/analyze")
async def analyze(request: ChangeRequest) -> Dict[str, Any]:
    change_text = request.change_text.strip()

    if not change_text:
        raise HTTPException(status_code=400, detail="No change description provided.")

    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured.")

    try:
        logging.info(f"🔍 Received request to analyze: {change_text}")
        logging.info(f"🔑 GEMINI_API_KEY status: {'SET' if GEMINI_API_KEY else 'NOT SET'}")

        # Generate a unique ID for this change request
        change_request_id = str(uuid.uuid4())

        # Call analyze_change_request with the generated ID and API key
        result = analyze_change_request(change_request_id, change_text, GEMINI_API_KEY)

        logging.info(f"✅ Analysis result: {result}")
        return result

    except Exception as e:
        logging.exception("🔥 Exception occurred while analyzing request:")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
