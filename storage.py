import cloudinary
import cloudinary.uploader
from config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)

def upload_to_cloudinary(url):
    """
    Uploads raw image bytes to Clouadinary.
    Returns secure URL.
    """
    result = cloudinary.uploader.upload(
        # file_bytes,
        # folder=folder,
        url
    )
    return result['secure_url']