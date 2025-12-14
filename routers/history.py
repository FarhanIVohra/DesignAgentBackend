from fastapi import APIRouter, HTTPException
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_ROLE

router = APIRouter(prefix="/history")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    raise ValueError("Supabase configuration is missing.")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# -------------------------------
# GET /history   → return list
# -------------------------------
@router.get("/")
def get_all_history():
    try:
        response = supabase.table("image_jobs").select("*").order("created_at", desc=True).execute()
        rows = response.data or []

        items = []
        for row in rows:
            image_url = (
                row.get("image_url") or
                row.get("final_image_url") or
                row.get("supabase_image_url") or
                row.get("supabase_url") or
                row.get("url")
            )

            seed = row.get("seed") or row.get("random_seed")

            items.append({
                "id": row.get("id"),
                "prompt": row.get("prompt"),
                "seed": seed,
                "image_url": image_url,
                "created_at": row.get("created_at")
            })

        return {"success": True, "count": len(items), "items": items}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# GET /history/{item_id} → single item
# -------------------------------
@router.get("/{item_id}")
def get_history_item(item_id: str):
    try:
        response = supabase.table("image_jobs").select("*").eq("id", item_id).single().execute()
        row = response.data
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")

        image_url = (
            row.get("image_url") or
            row.get("final_image_url") or
            row.get("supabase_image_url") or
            row.get("supabase_url") or
            row.get("url")
        )

        seed = row.get("seed") or row.get("random_seed")

        return {
            "id": row.get("id"),
            "prompt": row.get("prompt"),
            "seed": seed,
            "image_url": image_url,
            "created_at": row.get("created_at")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{item_id}")
def delete_history_item(item_id: str):
    try:
        res = supabase.table("image_jobs").delete().eq("id", item_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
