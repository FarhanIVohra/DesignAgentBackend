import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from config import OPENAI_API_KEY
router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/refine-prompt")
def refin_prompt(body: PromptRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY missing.")
    raw_prompt = body.prompt.strip()
    
    if not raw_prompt:
        raise HTTPException(status_code=400, detail="Empty Prompt")
    
    #Simple + cheap GPT-based refinement
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Rewrite the user prompt into a highly descriptive, clean, structured image generation prompt. Keep the meaning. Improve quality.Keep final result short."},
            {"role": "user", "content": raw_prompt}
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)
    
    refined = response.json()["choices"][0]["message"]["content"]
    
    return {
        "success": True,
        "original_prompt": raw_prompt,
        "refined_prompt": refined
    }