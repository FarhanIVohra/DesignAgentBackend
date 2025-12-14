import json
import requests
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import BRIA_API_KEY
from storage_utils import upload_image_bytes_to_supabase

router = APIRouter()

class VariantRequest(BaseModel):
    prompt: str
    count: int = 4  # how many variants to generate


@router.post("/generate-variants")
def generate_variants(body: VariantRequest):
    prompt = body.prompt
    count = body.count

    bria_url = "https://engine.prod.bria-api.com/v2/image/generate"

    headers = {
        "api_token": BRIA_API_KEY,
        "Content-Type": "application/json"
    }

    results = []

    for i in range(count):
        payload = {
            "prompt": prompt,
            "resolution": "1024x1024",
            "num_images": 1,
            "sync": True
        }

        # ---- Call BRIA ----
        bria_response = requests.post(
            bria_url,
            headers=headers,
            data=json.dumps(payload)
        )

        if bria_response.status_code != 200:
            raise HTTPException(
                status_code=bria_response.status_code,
                detail=bria_response.text
            )

        result = bria_response.json().get("result", {})
        image_url = result.get("image_url")
        seed = result.get("seed")

        if not image_url:
            raise HTTPException(500, "Bria did not return image_url")

        # ---- Download the image bytes ----
        img = requests.get(image_url)
        if img.status_code != 200:
            raise HTTPException(500, "Could not download Bria image")

        # ---- Upload to Supabase ----
        supabase_url = upload_image_bytes_to_supabase(
            img.content,
            extension="png",
            folder="variants"
        )

        results.append({
            "seed": seed,
            "image_url": supabase_url
        })

        # slight delay to avoid rate limits
        time.sleep(0.2)

    return {
        "success": True,
        "count": len(results),
        "items": results
    }
