from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os

router = APIRouter()

BRIA_API_KEY = os.getenv("BRIA_API_KEY")

if not BRIA_API_KEY:
    raise RuntimeError("BRIA_API_KEY is missing")

BRIA_GENFILL_URL = "https://engine.prod.bria-api.com/v2/image/edit/gen_fill"


class EditImageRequest(BaseModel):
    image_url: str
    mask_base64: str
    prompt: str


@router.post("/edit-image")
def edit_image(body: EditImageRequest):
    print("➡️ Image URL:", body.image_url)
    print("➡️ Prompt:", body.prompt)
    print("➡️ Mask length:", len(body.mask_base64))

    # ✅ HEADERS MUST ALWAYS EXIST
    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_KEY
    }

    payload = {
        "image": body.image_url,
        "mask": body.mask_base64,
        "prompt": body.prompt,
        "version": 2,
        "sync": True
    }

    print("📤 Sending request to BRIA...")

    try:
        response = requests.post(
            BRIA_GENFILL_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
    except Exception as e:
        print("❌ Network error:", e)
        raise HTTPException(status_code=500, detail=str(e))

    print("📥 BRIA STATUS:", response.status_code)
    print("📥 BRIA RESPONSE:", response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Bria API error: {response.text}"
        )

    data = response.json()

    # Handle both sync & async responses
    if "result" in data and "image_url" in data["result"]:
        return {"result_url": data["result"]["image_url"]}

    if "image_url" in data:
        return {"result_url": data["image_url"]}

    return {"raw_response": data}
