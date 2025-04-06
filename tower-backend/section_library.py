import json
import os
from dotenv import load_dotenv
from google.cloud import storage

# ✅ Load .env variables
load_dotenv()

# ✅ Extract environment variables
gcs_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
bucket_name = os.getenv("BUCKET_NAME")

# ✅ Sanity checks
if not gcs_key_path or not os.path.exists(gcs_key_path):
    raise FileNotFoundError(f"❌ GCS key not found at {gcs_key_path}")
if not bucket_name:
    raise ValueError("❌ BUCKET_NAME not set in .env")

# ✅ Set up credentials for GCS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcs_key_path

# ✅ Load local section data
with open("section_library.json", "r") as f:
    section_data = json.load(f)

# ✅ Upload to nested folder in GCS
client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob("sections/element_sections/section_library.json")  # 👈 Nested path
blob.upload_from_string(json.dumps(section_data), content_type="application/json")

print("✅ section_library.json uploaded to sections/element_sections/ in GCS.")
