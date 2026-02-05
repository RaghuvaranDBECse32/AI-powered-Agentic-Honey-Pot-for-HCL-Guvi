from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import os
import re

app = FastAPI()

API_KEY = os.getenv("API_KEY")

@app.post("/honeypot")
async def honeypot(request: Request, x_api_key: str = Header(None)):
    try:
        # --- API KEY CHECK ---
        if x_api_key != API_KEY:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid API Key"}
            )

        data = await request.json()
        message = str(data.get("message", "")).lower()

        # --- SCAM DETECTION ---
        scam_words = [
            "bank", "upi", "account", "otp",
            "verify", "blocked", "click", "refund", "kyc"
        ]
        scam_detected = any(word in message for word in scam_words)

        # --- EXTRACTION ---
        upi = re.search(r"\b[\w.-]+@[\w.-]+\b", message)
        bank = re.search(r"\b\d{9,18}\b", message)
        url = re.search(r"https?://\S+", message)

        extracted_data = {
            "upi_id": upi.group(0) if upi else None,
            "bank_account": bank.group(0) if bank else None,
            "phishing_url": url.group(0) if url else None
        }

        response_msg = (
            "Sure, please share more details so I can check."
            if scam_detected else
            "Hello, how can I assist you today?"
        )

        return {
            "scam_detected": scam_detected,
            "agent_activated": scam_detected,
            "response_message": response_msg,
            "extracted_intelligence": extracted_data
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error"}
        )


@app.get("/")
def health_check():
    return {"status": "Honeypot running"}
