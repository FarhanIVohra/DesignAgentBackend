from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import SUPABASE_URL, SUPABASE_ANON_KEY
from routers import jobs
from routers import generate
from routers.generate_image import router as image_router
from routers.history import router as history_router
from routers.generate_variants import router as variants_router
from routers.refine_prompt import router as refine_router
from routers.edit_image import router as edit_router

print("Supabase URL loaded:", bool(SUPABASE_URL))
app = FastAPI(
    title="DesignAgent Backend",
    description="Backend API for the DesignAgent - Autonomous Design Iteration with FIBO",
    version="0.1.0",
)

# from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://design-agent-frontend-a430o4csb-farhanivohras-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """
    Simple health endpoint to we can verify backend is running.
    Frontend or Postman can call this.
    """
    return {"status":"ok", "service":"designagent-backend"}

app.include_router(jobs.router)
app.include_router(generate.router)
app.include_router(image_router)
app.include_router(history_router)
app.include_router(variants_router)
app.include_router(refine_router)
app.include_router(edit_router)
# app.include_router(generate_image.router)
