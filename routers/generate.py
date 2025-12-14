from fastapi import APIRouter
from supabase_client import get_supabase
from llm_agent import generate_visual_json

router = APIRouter()

@router.post("/generate-initial/")
def generate_initial(job_id: str):
    supabase = get_supabase()
    
    #1. Fetch job record to get concept + imagae_url
    job = supabase.table("jobs").select("*").eq("id", job_id).single().execute()
    concept = job.data["concept"]
    image_url = job.data["image_url"]
    
    #2. Generate visual JSON
    visual_json = generate_visual_json(concept, image_url)
    
    #3. Save JSON + update status
    supabase.table("jobs").update({
        "visual_json": visual_json,
        "status": "json_ready"
    }).eq("id", job_id).execute()
    
    return {
        "job_id": job_id,
        "status": "json_ready",
        "visual_json": visual_json
    }