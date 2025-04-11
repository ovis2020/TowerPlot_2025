import os
import json
from google.cloud import storage
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Set GCS credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ✅ Define bucket
bucket_name = os.getenv("BUCKET_NAME", "towerbucket1")

# ✅ Path to your section_library.json
json_path = "C:/Users/rfuen/Desktop/TowerPlot/tower-backend/section_library.json"

# ✅ Load the JSON file
with open(json_path, "r") as f:
    section_data = json.load(f)

# ✅ Upload to Google Cloud Storage
client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob("sections/element_sections/section_library.json")  # 👈 this must match app.py
blob.upload_from_string(json.dumps(section_data), content_type="application/json")

print("✅ Uploaded section_library.json to GCS at sections/element_sections/")
