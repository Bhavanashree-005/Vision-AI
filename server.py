"""VisionCode AI — FastAPI Backend Server.

Runs natively on http://127.0.0.1:8000
"""

from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path
from typing import Optional

from PIL import Image
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Ensure workspace root is in python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.ai_service import AIService
from src.config import get_api_key, logger, set_api_key
from src.cv_engine import CVEngine

app = FastAPI(title="VisionCode AI Server", version="2.0.0")

# Enable CORS for local testing flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instance
ai_service = AIService()

# Ensure static directory exists
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)


# Helper: Convert BGR or Grayscale numpy image to Base64 JPEG string
def np_image_to_base64(img_np: np.ndarray) -> str:
    if len(img_np.shape) == 2:  # Grayscale
        success, encoded = cv2.imencode(".jpg", img_np)
    else:  # BGR
        success, encoded = cv2.imencode(".jpg", img_np)

    if not success:
        raise ValueError("Failed to encode processed image to JPEG.")

    b64_bytes = base64.b64encode(encoded.tobytes()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_bytes}"


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------


@app.get("/api/status")
def get_status():
    """Return backend configuration status."""
    return {
        "status": "online",
        "api_key_configured": ai_service.has_api_key,
        "default_model": "google/gemini-2.5-flash",
    }


@app.post("/api/config/api_key")
def update_api_key(api_key: str = Form(...)):
    """Update OpenRouter API key."""
    key = api_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="API key cannot be empty.")

    ai_service.update_api_key(key)
    return {"success": True, "message": "API key saved successfully!"}


@app.post("/api/cv/process")
async def process_cv_operation(
    file: UploadFile = File(...),
    task_category: str = Form(...),
    operation: str = Form(...),
    params_json: str = Form("{}"),
):
    """Process an image using OpenCV engine."""
    try:
        # Read image bytes and convert to BGR numpy array
        contents = await file.read()
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
        img_np = np.array(pil_img)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        params = json.loads(params_json)

        processed_img = None
        code = ""
        meta = {}

        if task_category == "Basic Filters":
            processed_img, code, meta = CVEngine.apply_basic_filter(
                img_bgr, operation, params
            )
        elif task_category == "Edge & Line Detection":
            processed_img, code, meta = CVEngine.apply_edge_detection(
                img_bgr, operation, params
            )
        elif task_category == "Contour Analytics":
            processed_img, code, meta = CVEngine.apply_contour_analysis(
                img_bgr, params
            )
        elif task_category == "Face & Eye Tracking":
            processed_img, code, meta = CVEngine.detect_faces_and_eyes(img_bgr)
        else:
            raise HTTPException(status_code=400, detail="Invalid task category.")

        image_b64 = np_image_to_base64(processed_img)

        return {
            "success": True,
            "image_b64": image_b64,
            "code": code,
            "metadata": meta,
        }
    except Exception as exc:
        logger.exception("CV processing failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/ai/task")
def run_ai_task(
    task: str = Form(...),
    user_input: str = Form(...),
):
    """Execute AI tasks (generate, explain, debug, improve, comment, chat)."""
    try:
        result = ""
        if task == "generate":
            result = ai_service.generate_code(user_input)
        elif task == "explain":
            result = ai_service.explain_code(user_input)
        elif task == "debug":
            result = ai_service.debug_error(user_input)
        elif task == "improve":
            result = ai_service.improve_code(user_input)
        elif task == "comment":
            result = ai_service.add_comments(user_input)
        elif task == "chat":
            result = ai_service.chat(user_input)
        else:
            raise HTTPException(status_code=400, detail="Unknown AI task.")

        return {"success": True, "result": result}
    except Exception as exc:
        logger.exception("AI Task execution failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/ai/vision")
async def run_ai_vision(
    query: str = Form(...),
    file: UploadFile = File(...),
):
    """Multi-modal vision AI analysis for screenshots and diagrams."""
    try:
        contents = await file.read()
        mime_type = file.content_type or "image/jpeg"
        result = ai_service.vision_analyze(query, contents, mime_type)
        return {"success": True, "result": result}
    except Exception as exc:
        logger.exception("AI Vision execution failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/ai/clear_history")
def clear_chat_history():
    """Clear chat memory."""
    ai_service.reset_history()
    return {"success": True, "message": "History cleared."}


# Serve static directory files at root
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    import io
    print("\n" + "=" * 60)
    print("VisionCode AI Local Server starting on http://127.0.0.1:8000")
    print("=" * 60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
