from fastapi import APIRouter, UploadFile, File
from supabase_client import get_supabase
router = APIRouter()

@router.get("/jobs/")
def create_job(concept: str, image_url: str=None):
    supabase = get_supabase()
    result = supabase.table("jobs").insert({
        "concept": concept,
        "image_url": image_url,
        "status": "pending"
    }).execute()
    
    return{
        "job_id": result.data[0]["id"],
        "status": "pending"
    }

@router.post("/jobs/upload-image")
async def upload_job_image(job_id: str, file: UploadFile = File(...)):
    from storage import upload_to_cloudinary
    from supabase_client import get_supabase
    
    #read binary data
    file_bytes = await file.read()
    
    #upload to cloudinary
    url = upload_to_cloudinary(file_bytes)
    
    #save url to database
    supabase = get_supabase()
    supabase.table("jobs").update({"image_url": url}).eq("id", job_id).execute()
    
    return {
        "job_id" : job_id,
        "image_url": url
    }    