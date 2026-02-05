from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

# Load API key from environment
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set")

# -------- Request Schema --------
class ScamRequest(BaseModel):
    message: str
    history: list = []

# -------- API KEY CHECK --------
def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# -------- MAIN ENDPOINT --------
@app.post("/honeypot")
def honeypot(
    data: ScamRequest,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    scam_detected = any(word in data.message.lower() for word in [
        "otp", "kyc", "account", "blocked", "verify", "link"
    ])

    response = {
        "scam_detected": scam_detected,
        "agent_activated": scam_detected,
        "engagement": {
            "turns": len(data.history) + 1,
            "status": "active" if scam_detected else "ignored"
        },
        "extracted_intelligence": {
            "bank_account": None,
            "upi_id": None,
            "phishing_url": None
        }
    }

    return response

# -------- HEALTH CHECK --------
@app.get("/")
def root():
    return {"status": "Honeypot API running"}
