# ─────────────────────────────────────────────────────────────────────────────
# uv-demo/main.py  — FastAPI Math Server
# ─────────────────────────────────────────────────────────────────────────────
#
# SETUP (run once in your uv-demo folder):
#   uv init
#   uv add fastapi uvicorn python-dotenv
#
# CREATE .env in the uv-demo folder:
#   API_SECRET_KEY=my-super-secret-key-123
#
# RUN:
#   uv run uvicorn main:app --reload
#
# TEST (from terminal):
#   curl -X POST http://127.0.0.1:8000/add \
#        -H "X-API-Key: my-super-secret-key-123" \
#        -H "Content-Type: application/json" \
#        -d '{"a": 10, "b": 5}'
# ─────────────────────────────────────────────────────────────────────────────

import math
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

load_dotenv()

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Math API",
    description="Simple math operations — used for AI Bootcamp async demos",
    version="1.0.0",
)

# ── Secret key (loaded from .env) ─────────────────────────────────────────────
SECRET_KEY = os.getenv("API_SECRET_KEY", "Novi@123")


# ── Request model ─────────────────────────────────────────────────────────────
class MathInput(BaseModel):
    a: float
    b: Optional[float] = None   # b is optional — sqrt only needs a


# ── Auth dependency ───────────────────────────────────────────────────────────
def verify_key(x_api_key: str = Header(...)):
    # FastAPI reads the X-API-Key header automatically
    # Header(...) means it's required — 422 if missing
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    # Quick check — open this in the browser to confirm server is up
    return {"status": "running", "version": "1.0.0"}


@app.post("/add")
async def add(body: MathInput, key: str = Depends(verify_key)):
    return {"operation": "add", "result": body.a + body.b}


@app.post("/subtract")
async def subtract(body: MathInput, key: str = Depends(verify_key)):
    return {"operation": "subtract", "result": body.a - body.b}


@app.post("/multiply")
async def multiply(body: MathInput, key: str = Depends(verify_key)):
    return {"operation": "multiply", "result": body.a * body.b}


@app.post("/divide")
async def divide(body: MathInput, key: str = Depends(verify_key)):
    if body.b is None or body.b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"operation": "divide", "result": body.a / body.b}


@app.post("/sqrt")
async def sqrt(body: MathInput, key: str = Depends(verify_key)):
    if body.a < 0:
        raise HTTPException(
            status_code=400, detail="Cannot take sqrt of a negative number"
        )
    return {"operation": "sqrt", "result": math.sqrt(body.a)}
