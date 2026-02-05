from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import os
import re

app = FastAPI()

# API KEY (from Vercel Environment Variable)
API_KEY = os.getenv("API_KEY", "CHANGE_ME")

@app.post("/api/honeypot")
async def honeypot(request: Request, x_api_key: str = Header(None)):
    try:
        # --- AUTH CHECK ---
        if x_api_key != API_KEY:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid API key"}
            )

        data = await request.json()

        message = str(data.get("message", "")).lower()

        # --- BASIC SCAM DETECTION ---
        scam_keywords = [
            "bank", "account", "upi", "verify", "blocked",
            "otp", "click", "link", "refund", "kyc"
        ]

        scam_detected = any(word in message for word in scam_keywords)

        # --- EXTRACTION (SIMPLE & SAFE) ---
        upi_match = re.search(r"\b[\w.-]+@[\w.-]+\b", message)
        url_match = re.search(r"https?://\S+", message)
        bank_match = re.search(r"\b\d{9,18}\b", message)

        extracted = {
            "upi_id": upi_match.group(0) if upi_match else None,
            "bank_account": bank_match.group(0) if bank_match else None,
            "phishing_url": url_match.group(0) if url_match else None
        }

        # --- AGENT RESPONSE ---
        response_text = (
            "Thanks for informing me. Can you share more details?"
            if scam_detected else
            "Hello! How can I help you?"
        )

        return {
            "scam_detected": scam_detected,
            "agent_activated": scam_detected,
            "response_message": response_text,
            "extracted_intelligence": extracted
        }

    except Exception:
        # NEVER CRASH
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )
