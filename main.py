from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
import re

app = FastAPI()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY missing")

class ScamRequest(BaseModel):
    message: str
    history: list = []

def verify_key(key: str):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.post("/honeypot")
def honeypot(
    data: ScamRequest,
    x_api_key: str = Header(...)
):
    verify_key(x_api_key)

    msg = data.message.lower()

    scam_keywords = [
        "kyc", "otp", "verify", "blocked",
        "bank", "upi", "link", "account"
    ]

    scam_detected = any(k in msg for k in scam_keywords)

    # Simple extraction logic
    upi_match = re.search(r"\b[\w.-]+@[\w.-]+\b", msg)
    url_match = re.search(r"https?://\S+", msg)

    return {
        "scam_detected": scam_detected,
        "agent_activated": scam_detected,
        "engagement": {
            "turns": len(data.history) + 1,
            "status": "active" if scam_detected else "ignored"
        },
        "extracted_intelligence": {
            "bank_account": None,
            "upi_id": upi_match.group(0) if upi_match else None,
            "phishing_url": url_match.group(0) if url_match else None
        }
    }

@app.get("/")
def health():
    return {"status": "ok"}
