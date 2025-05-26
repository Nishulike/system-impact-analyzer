from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from impact_analyzer.analyzer import analyze_change_request  # ✅ Correct import assuming your folder is structured properly
import os

# ✅ Load env variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # ✅ Should be set in Railway or .env

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS to allow frontend (e.g., Netlify) to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your frontend domain (e.g., https://yoursite.netlify.app)
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API Endpoint
@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    change_text = data.get("change_text", "")
    
    if not change_text.strip():
        return {"error": "No change description provided."}

    try:
        # GooglePalm key is passed to analyzer
        result = analyze_change_request(change_text, GOOGLE_API_KEY)
        return result
    except Exception as e:
        return {"error": str(e)}  # 🛠️ Optional: add logging for better debugging
