from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import re
import os

API_KEY = os.getenv("API_KEY", "ai_honeypot_demo_key")

app = FastAPI(title="Agentic Honey-Pot")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------- WEB UI ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------- HONEYPOT API ----------
@app.post("/honeypot")
async def honeypot(
    data: dict,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message = data.get("message", "")

    scam_keywords = [
        "blocked", "verify", "otp", "bank",
        "account", "upi", "click", "link", "urgent"
    ]

    is_scam = any(word in message.lower() for word in scam_keywords)

    # Extract entities
    upi_ids = re.findall(r"\b[\w.-]+@[\w.-]+\b", message)
    links = re.findall(r"https?://\S+", message)
    accounts = re.findall(r"\b\d{9,18}\b", message)

    return {
        "scam_detected": is_scam,
        "engagement_status": "agent_active" if is_scam else "ignored",
        "conversation_turns": 1,
        "extracted_intelligence": {
            "upi_ids": upi_ids,
            "bank_accounts": accounts,
            "phishing_links": links
        }
    }
