import os
import requests
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import BRIA_API_KEY, SUPABASE_SERVICE_ROLE, SUPABASE_URL
from storage_utils import upload_image_bytes_to_supabase
from supabase import create_client

# ----------------------------------------------------
# Supabase Setup
# ----------------------------------------------------
# SUPABASE_URL = "https://uqyadhehybhgrsmxsxjx.supabase.co"
# SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_ROLE:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY missing from .env")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# ----------------------------------------------------
# Router + Request Model
# ----------------------------------------------------
router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str

if not BRIA_API_KEY:
    raise ValueError("BRIA_API_KEY is missing. Add it to .env!")

# ----------------------------------------------------
# Main Route
# ----------------------------------------------------
@router.post("/generate-image")
def generate_image(body: ImageRequest):

    prompt = body.prompt

    # -------------------------------
    # 1) Call BRIA API
    # -------------------------------
    bria_url = "https://engine.prod.bria-api.com/v2/image/generate"

    headers = {
        "api_token": BRIA_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "resolution": "1024x1024",
        "num_images": 1,
        "sync": True
    }

    bria_response = requests.post(bria_url, headers=headers, data=json.dumps(payload))

    if bria_response.status_code != 200:
        raise HTTPException(status_code=bria_response.status_code, detail=bria_response.text)

    result = bria_response.json().get("result", {})
    bria_image_url = result.get("image_url")
    seed = result.get("seed")
    structured_prompt = result.get("structured_prompt")

    if not bria_image_url:
        raise HTTPException(status_code=500, detail="Bria did not return image_url")

    # -------------------------------
    # 2) Download Image Bytes
    # -------------------------------
    img_resp = requests.get(bria_image_url)
    if img_resp.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download image from Bria: {img_resp.status_code}"
        )

    image_bytes = img_resp.content

    # -------------------------------
    # 3) Upload to Supabase Storage
    # -------------------------------
    try:
        supabase_url = upload_image_bytes_to_supabase(image_bytes, extension="png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload to Supabase failed: {str(e)}")

    # -------------------------------
    # 4) Insert job record in database
    # -------------------------------
    try:
        insert_payload = {
            "prompt": prompt,
            "structured_prompt": structured_prompt,
            "seed": seed,
            "image_url": supabase_url
        }

        supabase.table("image_jobs").insert(insert_payload).execute()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insert failed: {str(e)}")

    # -------------------------------
    # 5) Return final JSON response
    # -------------------------------
    return {
        "success": True,
        "prompt": prompt,
        "seed": seed,
        "structured_prompt": structured_prompt,
        "bria_image_url": bria_image_url,
        "final_image_url": supabase_url
    }
