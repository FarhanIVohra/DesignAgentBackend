import os
from dotenv import load_dotenv
from fal_client import client

load_dotenv()

FAL_KEY = os.getenv("FAL_KEY")

fal = client.SyncClient(key=FAL_KEY)   # ⭐ Correct initialization
print("FAL connected successfully")
