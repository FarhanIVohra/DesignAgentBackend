import time
from io import BytesIO
from supabase import create_client

from config import SUPABASE_URL, SUPABASE_SERVICE_ROLE

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

BUCKET = "generated-images"


def upload_image_bytes_to_supabase(bytes_data, extension="png", folder="generated-images"):
    """Upload raw image bytes to Supabase with correct MIME type."""

    filename = f"{int(time.time() * 1000)}.{extension}"

    # Folder-safe path
    path = f"{folder}/{filename}"

    # Explicit content type FIX
    file_options = {
        "content-type": f"image/{extension}"
    }

    res = supabase.storage.from_(BUCKET).upload(
        path,
        bytes_data,
        file_options  # <-- THIS LINE FIXES THE ISSUE
    )

    # Some Supabase SDK versions return dict, others return object
    try:
        if hasattr(res, "error") and res.error:
            raise Exception(res.error)
    except:
        pass

    public_url = (
        f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{path}"
    )

    return public_url
