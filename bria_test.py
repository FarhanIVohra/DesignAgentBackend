import os
import requests
import json
from config import BRIA_API_KEY

# BRIA_API_KEY = BRIA_API_KEY

if not BRIA_API_KEY:
    raise ValueError("BRIA_API_KEY is missing in environment variables!")

def generate_image(prompt: str):
    url = "https://engine.prod.bria-api.com/v2/image/generate"

    # IMPORTANT — EXACT header format Bria requires
    headers = {
        "api_token": BRIA_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "resolution": "1024x1024",
        "num_images": 1,
        "sync": True     # sync == execute immediately
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status:", response.status_code)
    print("Response:", response.text)

    # If success
    if response.status_code == 200:
        data = response.json()
        return data.get("result", {}).get("image_url")

    return None


if __name__ == "__main__":
    img = generate_image("A fluffy cute baby owl sitting on a branch, moonlight, ultra realistic")
    print("Generated image:", img)
